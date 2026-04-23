# How to Run the CTTAF Benchmark

This guide walks through running an evaluation of your LLM on the CTTAF benchmark.

## Prerequisites

1. **API Keys**: Set up credentials for your target LLM and judges:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

2. **Environment**: Install dependencies
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r evaluation/requirements.txt
   ```

## Quick Start (Sample Dataset)

Run evaluation on 100 sample questions:

```bash
cd evaluation
python scripts/evaluate_model.py --model gpt-4 --output results/gpt4_sample.json
```

## Full Benchmark (900 Questions)

For the complete benchmark:

```bash
python scripts/evaluate_model.py --model gpt-4 \
  --questions ../data/questions/cttaf_questions_full_900.csv \
  --output results/gpt4_full.json
```

## Aggregating Results

After evaluation completes, compute final scores and statistics:

```bash
python scripts/aggregate_results.py --results results/gpt4_full.json --output results/gpt4_summary.json
```

## Validating Judge Agreement

Check inter-judge consistency:

```bash
python scripts/validate_judges.py --results results/gpt4_full.json
```

## Output Format

Results are structured as JSON:

```json
{
  "model": "gpt-4",
  "questions": [
    {
      "question_id": "q001",
      "question_text": "...",
      "response": "...",
      "judges": [
        {
          "judge": "openai",
          "scores": {
            "theological_accuracy": 85,
            "denominational_sensitivity": 90,
            "biblical_grounding": 82,
            "practical_applicability": 88,
            "intellectual_honesty": 85
          },
          "composite": 86
        },
        {
          "judge": "anthropic",
          "scores": { ... },
          "composite": 84
        }
      ],
      "geometric_mean": 85.0
    }
  ],
  "summary": {
    "average_score": 72.5,
    "tier_breakdown": { ... },
    "cohens_kappa": 0.65
  }
}
```

## Benchmarking Multiple Models

Run evaluations in sequence or parallel:

```bash
# Sequential
for model in gpt-4 claude-opus grok; do
  python scripts/evaluate_model.py --model $model --output results/${model}.json
done

# Parallel (requires GNU parallel or xargs)
echo "gpt-4 claude-opus grok" | xargs -n1 -P3 \
  python scripts/evaluate_model.py --model {} --output results/{}.json
```

## Troubleshooting

**Rate Limits**: The dual-judge evaluation will hit API rate limits on large datasets. Use exponential backoff or request increases.

**Cost**: 900 questions × 2 judges × multiple calls = significant API costs. Start with the 100-sample dataset for testing.

**Judge Disagreement**: High kappa disagreement may indicate ambiguous questions or judge miscalibration. See judge_instructions_full.md.

## Next Steps

- Review rubric details in `../rubric/cttaf_rubric_v1.0.md`
- Study judge instructions in `../appendices/judge_instructions_full.md`
- Contribute improvements: see `../CONTRIBUTING.md`
