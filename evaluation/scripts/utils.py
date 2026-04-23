"""
Utility functions for CTTAF benchmark evaluation
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any
import math

def load_csv(filepath: str) -> List[Dict[str, Any]]:
    """Load questions from CSV file."""
    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))

def load_json(filepath: str) -> Dict[str, Any]:
    """Load data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Save data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def geometric_mean(a: float, b: float) -> float:
    """Compute geometric mean of two scores."""
    if a < 0 or b < 0:
        return 0
    return math.sqrt(a * b)

def compute_composite_score(dimension_scores: List[float]) -> float:
    """Compute composite score from five dimensions."""
    return sum(dimension_scores) / len(dimension_scores)

def compute_cohens_kappa(judge1_scores: List[int], judge2_scores: List[int]) -> float:
    """
    Compute Cohen's kappa for inter-judge agreement.
    Bins scores into categories for discrete comparison.
    """
    # TODO: Implement Cohen's kappa calculation
    pass
