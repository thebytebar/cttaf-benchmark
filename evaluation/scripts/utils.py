"""
Comprehensive utilities for CTTAF benchmark evaluation.

Provides:
- CSV loading and validation
- Judge output parsing (strict JSON + fallback recovery)
- Result schema and validation
- API retry logic with exponential backoff
- Progress tracking and logging
- ICC (Intra-class Correlation) for inter-judge reliability
"""

import csv
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('benchmark.log')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class JudgeDimensionScore:
    """Single dimension score from one judge."""
    doctrinal_accuracy: int  # 0-100
    internal_coherence: int  # 0-100
    pastoral_sensitivity: int  # 0-100
    composite: int  # Calculated weighted score


@dataclass
class JudgeResult:
    """Complete evaluation from one judge."""
    judge: str  # "openai" or "anthropic"
    dimensions: JudgeDimensionScore
    parse_method: str  # "json" or "regex_recovered"
    raw_output: str
    error: Optional[str] = None


@dataclass
class QuestionResult:
    """Complete evaluation result for one question."""
    question_id: str
    question_text: str
    tier: str  # Primary/Secondary/Tertiary
    dimension: str
    denomination: str
    model_response: str
    judges: List[JudgeResult]
    geometric_mean: Optional[float]
    completion_status: str  # "complete", "incomplete", "parse_failed"
    disagreement_flagged: bool = False
    disagreement_delta: Optional[float] = None


def load_csv(filepath: str) -> List[Dict[str, Any]]:
    """Load questions from CSV file with validation."""
    questions = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required_cols = {'id', 'question_id', 'tier', 'dimension', 'denomination', 'question_text'}
            if not required_cols.issubset(reader.fieldnames or set()):
                raise ValueError(f"CSV missing required columns. Found: {reader.fieldnames}")
            
            for row_num, row in enumerate(reader, start=2):
                if not row.get('question_text', '').strip():
                    logger.warning(f"Row {row_num}: Skipping question with empty text")
                    continue
                questions.append(row)
        
        logger.info(f"Loaded {len(questions)} questions from {filepath}")
        return questions
    except FileNotFoundError:
        logger.error(f"Question file not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading questions: {e}")
        raise


def load_json(filepath: str) -> Dict[str, Any]:
    """Load data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Save data to JSON file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def parse_judge_output(raw_output: str) -> Tuple[Optional[JudgeDimensionScore], str]:
    """
    Parse judge output into structured scores.
    
    Returns:
        (JudgeDimensionScore, method) where method is "json" or "regex_recovered"
        (None, method) if parsing fails
    """
    # Try strict JSON first
    try:
        data = json.loads(raw_output)
        if _validate_judge_json(data):
            score = JudgeDimensionScore(
                doctrinal_accuracy=data['doctrinal_accuracy'],
                internal_coherence=data['internal_coherence'],
                pastoral_sensitivity=data['pastoral_sensitivity'],
                composite=data['composite']
            )
            return score, "json"
    except (json.JSONDecodeError, KeyError):
        pass
    
    # Try flexible regex recovery
    try:
        score = _parse_with_regex(raw_output)
        if score:
            return score, "regex_recovered"
    except Exception as e:
        logger.debug(f"Regex recovery failed: {e}")
    
    return None, "failed"


def _validate_judge_json(data: Dict[str, Any]) -> bool:
    """Validate judge JSON output structure."""
    required = {'doctrinal_accuracy', 'internal_coherence', 'pastoral_sensitivity', 'composite'}
    if not required.issubset(data.keys()):
        return False
    for key in required:
        if not isinstance(data[key], int) or not (0 <= data[key] <= 100):
            return False
    return True


def _parse_with_regex(text: str) -> Optional[JudgeDimensionScore]:
    """Extract scores from natural language output using regex."""
    patterns = {
        'doctrinal_accuracy': r'Dimension 1.*?:.*?(\d+)/100',
        'internal_coherence': r'Dimension 2.*?:.*?(\d+)/100',
        'pastoral_sensitivity': r'Dimension 3.*?:.*?(\d+)/100',
        'composite': r'Final.*?Score.*?:.*?(\d+)/100'
    }
    
    scores = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            score = int(match.group(1))
            if not (0 <= score <= 100):
                return None
            scores[key] = score
    
    if len(scores) == 4:
        return JudgeDimensionScore(
            doctrinal_accuracy=scores['doctrinal_accuracy'],
            internal_coherence=scores['internal_coherence'],
            pastoral_sensitivity=scores['pastoral_sensitivity'],
            composite=scores['composite']
        )
    return None


def geometric_mean(a: float, b: float) -> float:
    """Compute geometric mean of two scores (0-100 scale)."""
    if a < 0 or b < 0:
        return 0
    return math.sqrt(a * b)

def compute_composite_score(dimension_scores: List[float]) -> float:
    """Compute composite score from dimension scores (simple average)."""
    if not dimension_scores:
        return 0
    return sum(dimension_scores) / len(dimension_scores)

def calculate_icc_2_1(scores: List[Tuple[float, float]]) -> float:
    """
    Calculate ICC(2,1) for inter-judge reliability on continuous scores.
    
    ICC(2,1): Two-way mixed, absolute agreement, single rater
    
    Args:
        scores: List of (judge1_score, judge2_score) tuples
    
    Returns:
        ICC coefficient (-1.0 to 1.0)
    """
    if len(scores) < 2:
        return 0
    
    scores_array = list(scores)
    n_items = len(scores_array)
    n_judges = 2
    
    # Calculate means
    judge1_scores = [s[0] for s in scores_array]
    judge2_scores = [s[1] for s in scores_array]
    
    mean_judge1 = sum(judge1_scores) / n_judges if judge1_scores else 0
    mean_judge2 = sum(judge2_scores) / n_judges if judge2_scores else 0
    grand_mean = (mean_judge1 + mean_judge2) / 2
    
    # Calculate sum of squares
    ss_total = sum((s[0] - grand_mean) ** 2 + (s[1] - grand_mean) ** 2 for s in scores_array)
    ss_judges = n_items * ((mean_judge1 - grand_mean) ** 2 + (mean_judge2 - grand_mean) ** 2)
    ss_error = ss_total - ss_judges
    
    # Calculate mean squares
    ms_judges = ss_judges / (n_judges - 1)
    ms_error = ss_error / ((n_judges - 1) * (n_items - 1))
    
    if ms_error == 0:
        return 1.0 if ms_judges == 0 else 1.0
    
    icc = (ms_judges - ms_error) / (ms_judges + (n_judges - 1) * ms_error)
    return max(-1.0, min(1.0, icc))  # Clamp to [-1, 1]

def retry_with_backoff(func, max_retries: int = 3, initial_delay: float = 1.0):
    """
    Decorator for API calls with exponential backoff retry.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of attempts
        initial_delay: Starting delay in seconds
    """
    def wrapper(*args, **kwargs):
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
        return None
    return wrapper


def save_checkpoint(results: List[QuestionResult], checkpoint_path: str):
    """Save results checkpoint for resumable runs."""
    data = {
        'timestamp': datetime.now().isoformat(),
        'num_results': len(results),
        'results': [_question_result_to_dict(r) for r in results]
    }
    Path(checkpoint_path).parent.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    logger.info(f"Checkpoint saved: {checkpoint_path} ({len(results)} results)")


def load_checkpoint(checkpoint_path: str) -> List[Dict]:
    """Load results from checkpoint."""
    if not Path(checkpoint_path).exists():
        return []
    with open(checkpoint_path, 'r') as f:
        data = json.load(f)
    logger.info(f"Loaded {len(data['results'])} results from checkpoint")
    return data['results']


def _question_result_to_dict(result: QuestionResult) -> Dict:
    """Convert QuestionResult to dictionary for JSON serialization."""
    return {
        'question_id': result.question_id,
        'question_text': result.question_text,
        'tier': result.tier,
        'dimension': result.dimension,
        'denomination': result.denomination,
        'model_response': result.model_response,
        'judges': [
            {
                'judge': j.judge,
                'dimensions': {
                    'doctrinal_accuracy': j.dimensions.doctrinal_accuracy,
                    'internal_coherence': j.dimensions.internal_coherence,
                    'pastoral_sensitivity': j.dimensions.pastoral_sensitivity,
                    'composite': j.dimensions.composite
                },
                'parse_method': j.parse_method,
                'error': j.error
            } for j in result.judges if not j.error
        ],
        'geometric_mean': result.geometric_mean,
        'completion_status': result.completion_status,
        'disagreement_flagged': result.disagreement_flagged,
        'disagreement_delta': result.disagreement_delta
    }
