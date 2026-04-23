"""
Mock evaluator for CTTAF benchmark - runs completely locally and free.

Supports:
1. Synthetic data generation (realistic judge scores)
2. Local open-source LLMs (Ollama, Hugging Face)
3. Full pipeline testing without API costs
"""

import argparse
import json
import logging
import random
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from utils import (
    load_csv, save_json, save_checkpoint, load_checkpoint,
    JudgeResult, JudgeDimensionScore, QuestionResult, geometric_mean, logger
)


class MockJudgeScore:
    """Generate realistic mock judge scores based on question characteristics."""
    
    def __init__(self, tier: str, seed: Optional[int] = None):
        """
        Initialize mock scorer.
        
        Args:
            tier: 'Primary', 'Secondary', or 'Tertiary'
            seed: Random seed for reproducibility
        """
        self.tier = tier
        if seed:
            random.seed(seed)
    
    def generate_score(self, quality_multiplier: float = 1.0) -> JudgeDimensionScore:
        """
        Generate a realistic score distribution.
        
        Quality scores vary by tier (Primary is stricter):
        - Primary: Higher baseline, less variance (stricter grading)
        - Secondary: Medium baseline and variance
        - Tertiary: Lower baseline, more variance (more lenient)
        
        Args:
            quality_multiplier: 0-2 scale. 1.0 = baseline, >1.0 = better, <1.0 = worse
        
        Returns:
            JudgeDimensionScore with realistic values
        """
        tier_params = {
            'Primary': {'base': 75, 'variance': 8, 'floor': 60},
            'Secondary': {'base': 70, 'variance': 12, 'floor': 45},
            'Tertiary': {'base': 68, 'variance': 15, 'floor': 40},
            'foundational': {'base': 75, 'variance': 8, 'floor': 60},
            'secondary': {'base': 70, 'variance': 12, 'floor': 45},
            'tertiary': {'base': 68, 'variance': 15, 'floor': 40},
        }
        
        params = tier_params.get(self.tier, tier_params['Secondary'])
        
        # Generate base scores
        base = params['base'] * quality_multiplier
        variance = params['variance']
        floor = params['floor'] * quality_multiplier
        
        # Dimension scores with slight variance
        doctrinal = max(floor, min(100, base + random.gauss(0, variance * 0.5)))
        coherence = max(floor, min(100, base + random.gauss(0, variance * 0.5)))
        pastoral = max(floor, min(100, base + random.gauss(0, variance * 0.7)))
        
        # Composite is weighted average
        composite = int((doctrinal * 0.4 + coherence * 0.35 + pastoral * 0.25))
        
        return JudgeDimensionScore(
            doctrinal_accuracy=int(doctrinal),
            internal_coherence=int(coherence),
            pastoral_sensitivity=int(pastoral),
            composite=composite
        )


class MockCTTAFBenchmark:
    """Mock evaluator that runs completely locally without API calls."""
    
    def __init__(self, model: str, output_dir: str, questions_path: str, seed: int = 42):
        """
        Initialize mock benchmark.
        
        Args:
            model: Model name (used in results, not called)
            output_dir: Where to save results
            questions_path: Path to questions CSV
            seed: Random seed for reproducible results
        """
        self.model = model
        self.output_dir = Path(output_dir)
        self.questions_path = questions_path
        self.seed = seed
        self.checkpoint_path = self.output_dir / f"checkpoint_{model}.json"
        self.results_path = self.output_dir / f"{model}_results.json"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        random.seed(seed)
        
        logger.info(f"Initialized mock evaluator for model: {model} (seed={seed})")
    
    def run(self, max_questions: Optional[int] = None, judge_variance: float = 1.0):
        """
        Run mock evaluation with synthetic judge outputs.
        
        Args:
            max_questions: Limit number of questions
            judge_variance: 0.5 = judges agree closely, 1.5 = judges disagree more
        """
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
                # Generate mock response
                model_response = self._generate_mock_response(question)
                
                # Generate judge evaluations
                judges = self._generate_mock_judges(question, judge_variance)
                
                # Calculate geometric mean
                if len(judges) == 2 and all(not j.error for j in judges):
                    geo_mean = geometric_mean(
                        judges[0].dimensions.composite,
                        judges[1].dimensions.composite
                    )
                    status = "complete"
                    delta = abs(judges[0].dimensions.composite - judges[1].dimensions.composite)
                    flagged = delta > 15
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
        logger.info(f"Mock evaluation complete. Results saved to {self.results_path}")
        return results
    
    def _generate_mock_response(self, question: dict) -> str:
        """Generate a realistic mock response."""
        templates = {
            'christology': [
                "Jesus Christ is the Son of God, the second person of the Trinity...",
                "Christ is fully God and fully human, as affirmed by the Council of Chalcedon...",
                "Jesus Christ is the central figure of Christian faith and redemption..."
            ],
            'soteriology': [
                "The gospel reveals God's plan of salvation through Christ's death and resurrection...",
                "Salvation comes through faith in Jesus Christ and His atoning work...",
                "The gospel is the good news that through Christ we can be reconciled to God..."
            ],
            'theodicy': [
                "Christian theology addresses suffering through the lens of God's sovereignty and love...",
                "Suffering, while difficult, can be understood through God's redemptive purposes...",
                "Christians find meaning in suffering through their union with Christ..."
            ],
            'default': [
                "This is an important theological question that reflects Christian doctrine...",
                "The biblical tradition addresses this through the lens of God's character...",
                "Various Christian perspectives offer insight into this matter..."
            ]
        }
        
        dimension = question.get('dimension', 'default').lower()
        template_list = templates.get(dimension, templates['default'])
        return random.choice(template_list)
    
    def _generate_mock_judges(self, question: dict, variance: float = 1.0) -> List[JudgeResult]:
        """Generate mock evaluations from two judges."""
        tier = question.get('tier', 'Secondary')
        
        judges = []
        for judge_name in ['openai', 'anthropic']:
            # Create separate scorer for each judge with different seed
            scorer = MockJudgeScore(tier, seed=self.seed + hash(judge_name) % 1000)
            
            # Quality varies by dimension
            quality = random.uniform(0.8, 1.2)
            
            # Generate base score
            score = scorer.generate_score(quality_multiplier=quality)
            
            # Add judge-specific variance (simulate judge disagreement)
            if variance > 1.0:
                # Increase variance for disagreement testing
                score.doctrinal_accuracy = int(
                    max(0, min(100, score.doctrinal_accuracy + random.gauss(0, 5 * variance)))
                )
                score.internal_coherence = int(
                    max(0, min(100, score.internal_coherence + random.gauss(0, 5 * variance)))
                )
                score.pastoral_sensitivity = int(
                    max(0, min(100, score.pastoral_sensitivity + random.gauss(0, 5 * variance)))
                )
                score.composite = int(
                    (score.doctrinal_accuracy * 0.4 +
                     score.internal_coherence * 0.35 +
                     score.pastoral_sensitivity * 0.25)
                )
            
            judges.append(JudgeResult(
                judge=judge_name,
                dimensions=score,
                parse_method="synthetic",
                raw_output=f"Mock output from {judge_name}"
            ))
        
        return judges
    
    def _save_results(self, results: List[QuestionResult]):
        """Save final results."""
        from utils import _question_result_to_dict
        
        data = {
            'model': self.model,
            'mode': 'mock',
            'timestamp': datetime.now().isoformat(),
            'num_questions': len(results),
            'num_complete': sum(1 for r in results if r.completion_status == 'complete'),
            'num_flagged': sum(1 for r in results if r.disagreement_flagged),
            'results': [_question_result_to_dict(r) for r in results]
        }
        
        save_json(data, str(self.results_path))


def main():
    parser = argparse.ArgumentParser(
        description="Run CTTAF benchmark locally with synthetic data (free, no API costs)"
    )
    parser.add_argument("--model", default="mock-gpt-4", 
                       help="Model name (for results labeling only)")
    parser.add_argument("--output", default="results",
                       help="Output directory for results")
    parser.add_argument("--questions", default="../../data/questions/cttaf_questions_sample_100.csv",
                       help="Path to questions CSV")
    parser.add_argument("--max-questions", type=int, default=None,
                       help="Limit number of questions")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed for reproducibility")
    parser.add_argument("--judge-variance", type=float, default=1.0,
                       help="Judge disagreement level (0.5=agree closely, 1.5=disagree more)")
    
    args = parser.parse_args()
    
    # Resolve relative paths
    questions_path = Path(args.questions)
    if not questions_path.is_absolute():
        questions_path = Path(__file__).parent.parent / questions_path
    
    logger.info(f"Starting mock CTTAF benchmark (local, free)")
    logger.info(f"  Model: {args.model}")
    logger.info(f"  Questions: {questions_path}")
    logger.info(f"  Output: {args.output}")
    logger.info(f"  Seed: {args.seed}")
    logger.info(f"  Judge variance: {args.judge_variance}")
    
    if not questions_path.exists():
        logger.error(f"Questions file not found: {questions_path}")
        sys.exit(1)
    
    benchmark = MockCTTAFBenchmark(
        model=args.model,
        output_dir=args.output,
        questions_path=str(questions_path),
        seed=args.seed
    )
    
    benchmark.run(
        max_questions=args.max_questions,
        judge_variance=args.judge_variance
    )


if __name__ == "__main__":
    main()
