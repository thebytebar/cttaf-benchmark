"""
Main evaluation script for CTTAF benchmark.

Orchestrates:
1. Loading theological questions
2. Querying target LLM
3. Dual-judge evaluation (OpenAI + Anthropic)
4. Result aggregation with geometric mean
5. Checkpoint-based resumable execution

Supported target models and their API providers are defined in
models_config.py.  Use --list-models to print all registered model IDs.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import time

from utils import (
    load_csv, parse_judge_output, geometric_mean, save_json,
    save_checkpoint, load_checkpoint, JudgeResult, JudgeDimensionScore,
    QuestionResult, logger
)

# Import API clients (required for the dual-judge pipeline)
try:
    from openai import OpenAI
except ImportError:
    logger.error("openai package not installed")
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    logger.error("anthropic package not installed")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()


class CTTAFBenchmarkEvaluator:
    """Main benchmark evaluator."""

    def __init__(self, model: str, output_dir: str, questions_path: str, dry_run: bool = False):
        self.model = model
        self.output_dir = Path(output_dir)
        self.questions_path = questions_path
        self.dry_run = dry_run
        self.checkpoint_path = self.output_dir / f"checkpoint_{model}.json"
        self.results_path = self.output_dir / f"{model}_results.json"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize judge API clients (skip in dry-run).
        # OPENAI_API_KEY and ANTHROPIC_API_KEY are required for the dual-judge
        # pipeline regardless of which model is being evaluated.
        if not dry_run:
            openai_key = os.getenv('OPENAI_API_KEY')
            anthropic_key = os.getenv('ANTHROPIC_API_KEY')

            if not openai_key or not anthropic_key:
                logger.error("Missing judge API keys. Set OPENAI_API_KEY and ANTHROPIC_API_KEY in .env")
                sys.exit(1)

            self.openai_client = OpenAI(api_key=openai_key)
            self.anthropic_client = Anthropic(api_key=anthropic_key)

            # Warn early if the target model's provider key is absent
            from model_providers import validate_model_api_key
            validate_model_api_key(model)
        else:
            self.openai_client = None
            self.anthropic_client = None

        logger.info(f"Initialized evaluator for model: {model}")
    
    def run(self, max_questions: Optional[int] = None):
        """Run benchmark evaluation."""
        # Load questions
        questions = load_csv(self.questions_path)
        if max_questions:
            questions = questions[:max_questions]
            logger.info(f"Limited to first {max_questions} questions")
        
        # Load checkpoint if resuming
        checkpoint_data = load_checkpoint(str(self.checkpoint_path))
        processed_ids = {r['question_id'] for r in checkpoint_data}
        
        results = []
        for i, question in enumerate(questions, 1):
            q_id = question['question_id']
            
            # Skip if already processed
            if q_id in processed_ids:
                logger.info(f"[{i}/{len(questions)}] Skipping {q_id} (already processed)")
                continue
            
            logger.info(f"[{i}/{len(questions)}] Evaluating {q_id}...")
            
            try:
                if self.dry_run:
                    logger.info(f"DRY RUN: Would evaluate {q_id}")
                    model_response = "[DRY RUN RESPONSE]"
                    geo_mean = 75.0
                    judges = []
                    status = "complete"
                    delta = 0
                    flagged = False
                else:
                    # Query target model
                    model_response = self._get_model_response(question['question_text'])
                    
                    # Get judge evaluations
                    judges = self._get_judge_evaluations(question, model_response)
                    
                    # Calculate geometric mean
                    if len(judges) == 2 and all(not j.error for j in judges):
                        geo_mean = geometric_mean(judges[0].dimensions.composite, judges[1].dimensions.composite)
                        status = "complete"
                        delta = abs(judges[0].dimensions.composite - judges[1].dimensions.composite)
                        flagged = delta > 15  # Flag if judges differ by >15 points
                    else:
                        geo_mean = None
                        status = "incomplete"
                        delta = None
                        flagged = False
                
                result = QuestionResult(
                    question_id=q_id,
                    question_text=question['question_text'],
                    tier=question.get('tier', 'Secondary'),
                    dimension=question.get('dimension', 'unknown'),
                    denomination=question.get('denomination', 'ecumenical'),
                    model_response=model_response,
                    judges=judges,
                    geometric_mean=geo_mean,
                    completion_status=status,
                    disagreement_flagged=flagged,
                    disagreement_delta=delta
                )
                
                results.append(result)
                
                # Periodic checkpoint
                if i % 10 == 0:
                    save_checkpoint(results, str(self.checkpoint_path))
            
            except Exception as e:
                logger.error(f"Error evaluating {q_id}: {e}", exc_info=True)
                continue
        
        # Final save
        self._save_results(results)
        logger.info(f"Evaluation complete. Results saved to {self.results_path}")
        return results
    
    def _get_model_response(self, question: str) -> str:
        """Query the target model via its registered API provider."""
        from model_providers import get_model_response
        return get_model_response(self.model, question)
    
    def _get_judge_evaluations(self, question: dict, response: str) -> List[JudgeResult]:
        """Get evaluations from both judges."""
        judges = []
        
        # OpenAI judge
        openai_result = self._query_judge(
            "openai",
            question,
            response,
            self._get_openai_judge_prompt(question, response)
        )
        judges.append(openai_result)
        
        # Small delay to avoid rate limits
        time.sleep(1)
        
        # Anthropic judge
        anthropic_result = self._query_judge(
            "anthropic",
            question,
            response,
            self._get_anthropic_judge_prompt(question, response)
        )
        judges.append(anthropic_result)
        
        return judges
    
    def _query_judge(self, judge_name: str, question: dict, response: str, judge_prompt: str) -> JudgeResult:
        """Query a single judge."""
        try:
            if judge_name == "openai":
                result = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": judge_prompt}],
                    temperature=0.0,
                    max_tokens=500
                )
                raw_output = result.choices[0].message.content
            else:  # anthropic
                result = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=500,
                    messages=[{"role": "user", "content": judge_prompt}]
                )
                raw_output = result.content[0].text
            
            # Parse output
            dimensions, parse_method = parse_judge_output(raw_output)
            
            if dimensions:
                return JudgeResult(
                    judge=judge_name,
                    dimensions=dimensions,
                    parse_method=parse_method,
                    raw_output=raw_output
                )
            else:
                return JudgeResult(
                    judge=judge_name,
                    dimensions=None,
                    parse_method="failed",
                    raw_output=raw_output,
                    error="Failed to parse judge output"
                )
        except Exception as e:
            logger.error(f"Error querying {judge_name} judge: {e}")
            return JudgeResult(
                judge=judge_name,
                dimensions=None,
                parse_method="failed",
                raw_output="",
                error=str(e)
            )
    
    def _get_openai_judge_prompt(self, question: dict, response: str) -> str:
        """Generate judge prompt for OpenAI."""
        return f"""You are an expert panel of Christian theologians evaluating LLM responses.

Question Tier: {question.get('tier', 'Unknown')}
Question Dimension: {question.get('dimension', 'Unknown')}
Denomination Context: {question.get('denomination', 'ecumenical')}

ORIGINAL QUESTION:
{question['question_text']}

MODEL RESPONSE:
{response}

Score this response on three dimensions (0-100):
1. Doctrinal Accuracy & Fidelity
2. Internal Coherence  
3. Pastoral Sensitivity & Application

Return ONLY valid JSON with no additional text:
{{
  "doctrinal_accuracy": <0-100>,
  "internal_coherence": <0-100>,
  "pastoral_sensitivity": <0-100>,
  "composite": <0-100>
}}"""
    
    def _get_anthropic_judge_prompt(self, question: dict, response: str) -> str:
        """Generate judge prompt for Anthropic."""
        return self._get_openai_judge_prompt(question, response)
    
    def _save_results(self, results: List[QuestionResult]):
        """Save final results."""
        from utils import _question_result_to_dict
        
        data = {
            'model': self.model,
            'timestamp': datetime.now().isoformat(),
            'num_questions': len(results),
            'num_complete': sum(1 for r in results if r.completion_status == 'complete'),
            'num_flagged': sum(1 for r in results if r.disagreement_flagged),
            'results': [_question_result_to_dict(r) for r in results]
        }
        
        save_json(data, str(self.results_path))


def main():
    parser = argparse.ArgumentParser(description="Evaluate LLM on CTTAF benchmark")
    parser.add_argument(
        "--model", required=False,
        help=(
            "Model to evaluate. Use a registered benchmark ID (e.g. gpt-5.4, "
            "claude-sonnet-4-6, gemini-3.1-pro, llama-4-maverick, grok-4, "
            "mistral-large, deepseek-v3, command-r-plus …) or a raw API "
            "model name. Run --list-models for the full list."
        )
    )
    parser.add_argument("--output", default="results", help="Output directory for results")
    parser.add_argument("--questions", default="../../data/questions/cttaf_questions_sample_100.csv",
                       help="Path to questions CSV")
    parser.add_argument("--max-questions", type=int, default=None, help="Limit number of questions (for testing)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without calling APIs")
    parser.add_argument("--list-models", action="store_true",
                       help="Print all registered benchmark model IDs and exit")

    args = parser.parse_args()

    if args.list_models:
        from models_config import MODEL_REGISTRY, NO_PUBLIC_API, PROVIDERS
        print("\nRegistered benchmark model IDs:")
        print("=" * 60)
        current_provider = None
        for mid in sorted(MODEL_REGISTRY.keys()):
            entry = MODEL_REGISTRY[mid]
            provider = entry["provider"]
            desc = PROVIDERS[provider]["description"]
            if provider != current_provider:
                print(f"\n  [{desc}]")
                current_provider = provider
            print(f"    {mid}  →  {entry['model_id']}")
        print("\nModels WITHOUT public API access:")
        print("=" * 60)
        for mid, note in NO_PUBLIC_API.items():
            print(f"  {mid}: {note}")
        print()
        sys.exit(0)

    if not args.model:
        parser.error("--model is required (or use --list-models to see available models)")

    # Resolve relative paths
    questions_path = Path(args.questions)
    if not questions_path.is_absolute():
        questions_path = Path(__file__).parent.parent / questions_path

    logger.info(f"Starting CTTAF benchmark evaluation")
    logger.info(f"  Model: {args.model}")
    logger.info(f"  Questions: {questions_path}")
    logger.info(f"  Output: {args.output}")

    if args.dry_run:
        logger.info("  Mode: DRY RUN (no API calls)")

    if not questions_path.exists():
        logger.error(f"Questions file not found: {questions_path}")
        sys.exit(1)

    evaluator = CTTAFBenchmarkEvaluator(
        model=args.model,
        output_dir=args.output,
        questions_path=str(questions_path),
        dry_run=args.dry_run
    )

    evaluator.run(max_questions=args.max_questions)


if __name__ == "__main__":
    main()

