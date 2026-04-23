"""
Aggregation script for CTTAF benchmark results.

Computes:
1. Tier-based score aggregation  
2. Inter-judge reliability (ICC)
3. Disagreement analysis
4. Summary statistics
5. Completion rates
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
from statistics import mean, stdev

from utils import load_json, save_json, calculate_icc_2_1, logger

# Configure logging
logging.basicConfig(level=logging.INFO)


def aggregate_results(results_path: str, output_path: str = None):
    """Aggregate benchmark results."""
    
    # Load results
    data = load_json(results_path)
    results = data['results']
    model = data.get('model', 'unknown')
    
    if not results:
        logger.error("No results to aggregate")
        return
    
    logger.info(f"Aggregating {len(results)} results for model: {model}")
    
    # Filter complete evaluations
    complete_results = [r for r in results if r.get('completion_status') == 'complete']
    logger.info(f"Complete evaluations: {len(complete_results)}/{len(results)} ({100*len(complete_results)/len(results):.1f}%)")
    
    # Calculate statistics by tier
    tier_stats = _calculate_tier_stats(complete_results)
    
    # Calculate inter-judge reliability
    icc_score = _calculate_icc(complete_results)
    
    # Disagreement analysis
    disagreement_stats = _analyze_disagreements(complete_results)
    
    # Overall statistics
    all_geometric_means = [r['geometric_mean'] for r in complete_results if r['geometric_mean'] is not None]
    
    overall_stats = {
        'model': model,
        'total_questions': len(results),
        'complete_evaluations': len(complete_results),
        'completion_rate': len(complete_results) / len(results),
        'average_score': mean(all_geometric_means) if all_geometric_means else 0,
        'score_stdev': stdev(all_geometric_means) if len(all_geometric_means) > 1 else 0,
        'min_score': min(all_geometric_means) if all_geometric_means else 0,
        'max_score': max(all_geometric_means) if all_geometric_means else 0,
        'tier_breakdown': tier_stats,
        'inter_judge_reliability_icc': icc_score,
        'disagreement_analysis': disagreement_stats
    }
    
    # Save summary
    if not output_path:
        output_path = Path(results_path).parent / f"{model}_summary.json"
    
    save_json(overall_stats, str(output_path))
    logger.info(f"Summary saved to {output_path}")
    
    # Print summary
    _print_summary(overall_stats)
    
    return overall_stats


def _calculate_tier_stats(results: List[Dict]) -> Dict:
    """Calculate statistics by tier."""
    tier_groups = defaultdict(list)
    
    for result in results:
        tier = result.get('tier', 'Unknown')
        if result['geometric_mean'] is not None:
            tier_groups[tier].append(result['geometric_mean'])
    
    tier_stats = {}
    for tier in ['Primary', 'Secondary', 'Tertiary', 'foundational', 'secondary', 'tertiary']:
        if tier in tier_groups and tier_groups[tier]:
            scores = tier_groups[tier]
            tier_stats[tier] = {
                'count': len(scores),
                'average': mean(scores),
                'stdev': stdev(scores) if len(scores) > 1 else 0,
                'min': min(scores),
                'max': max(scores)
            }
    
    return tier_stats


def _calculate_icc(results: List[Dict]) -> float:
    """Calculate ICC(2,1) for inter-judge reliability."""
    score_pairs = []
    
    for result in results:
        judges = result.get('judges', [])
        if len(judges) >= 2:
            score1 = judges[0].get('dimensions', {}).get('composite')
            score2 = judges[1].get('dimensions', {}).get('composite')
            
            if score1 is not None and score2 is not None:
                score_pairs.append((score1, score2))
    
    if not score_pairs:
        logger.warning("No score pairs for ICC calculation")
        return 0
    
    icc = calculate_icc_2_1(score_pairs)
    logger.info(f"Inter-judge ICC(2,1): {icc:.3f} (n={len(score_pairs)})")
    
    return icc


def _analyze_disagreements(results: List[Dict]) -> Dict:
    """Analyze judge disagreements."""
    flagged = [r for r in results if r.get('disagreement_flagged')]
    deltas = [r['disagreement_delta'] for r in results if r.get('disagreement_delta') is not None]
    
    return {
        'flagged_count': len(flagged),
        'flagged_percent': 100 * len(flagged) / len(results) if results else 0,
        'average_delta': mean(deltas) if deltas else 0,
        'max_delta': max(deltas) if deltas else 0,
        'flagged_examples': [
            {
                'question_id': r['question_id'],
                'delta': r['disagreement_delta'],
                'judge1_score': r['judges'][0]['dimensions']['composite'] if r['judges'] else None,
                'judge2_score': r['judges'][1]['dimensions']['composite'] if len(r['judges']) > 1 else None
            }
            for r in flagged[:5]  # Show first 5 examples
        ]
    }


def _print_summary(stats: Dict):
    """Print summary to console."""
    print("\n" + "="*60)
    print(f"CTTAF Benchmark Summary - Model: {stats['model']}")
    print("="*60)
    
    print(f"\nCompletion Rate: {stats['completion_rate']:.1%} ({stats['complete_evaluations']}/{stats['total_questions']})")
    print(f"Average Score: {stats['average_score']:.1f} ± {stats['score_stdev']:.1f}")
    print(f"Score Range: {stats['min_score']:.1f} - {stats['max_score']:.1f}")
    
    print(f"\nInter-Judge Reliability (ICC): {stats['inter_judge_reliability_icc']:.3f}")
    
    if stats['tier_breakdown']:
        print("\nTier Breakdown:")
        for tier, stats_data in stats['tier_breakdown'].items():
            print(f"  {tier}: {stats_data['average']:.1f} ({stats_data['count']} questions)")
    
    disagreement = stats['disagreement_analysis']
    print(f"\nJudge Disagreement: {disagreement['flagged_percent']:.1f}% flagged")
    print(f"  Average delta: {disagreement['average_delta']:.1f}")
    print(f"  Max delta: {disagreement['max_delta']:.1f}")
    
    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Aggregate CTTAF benchmark results")
    parser.add_argument("--results", required=True, help="Results JSON from evaluate_model.py")
    parser.add_argument("--output", default=None, help="Output file for summary (auto-generated if not specified)")
    
    args = parser.parse_args()
    
    if not Path(args.results).exists():
        logger.error(f"Results file not found: {args.results}")
        sys.exit(1)
    
    aggregate_results(args.results, args.output)


if __name__ == "__main__":
    main()

