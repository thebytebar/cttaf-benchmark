# CTTAF Benchmark - Quick Start

## 30-Second Setup

```bash
cd evaluation
pip3 install -r requirements.txt
cp ../.env.example ../.env
# Edit .env with your API keys
```

## Run Benchmark (3 Commands)

```bash
# 1. Test without API calls (verify setup)
python3 scripts/evaluate_model.py --model gpt-4 --dry-run --max-questions 3

# 2. Evaluate model on 100 questions
python3 scripts/evaluate_model.py --model gpt-4 --output results

# 3. Get summary statistics
python3 scripts/aggregate_results.py --results results/gpt-4_results.json
```

## Output Files

- `results/gpt-4_results.json` - Full evaluation data
- `results/gpt-4_summary.json` - Summary with inter-judge agreement

## What Gets Measured

| Metric | Meaning |
|--------|---------|
| Average Score | Mean geometric mean across all questions (0-100) |
| Tier Breakdown | Scores separated by theological importance (Primary/Secondary/Tertiary) |
| ICC Score | Inter-judge agreement (0.81-1.0 = excellent, <0.2 = poor) |
| Disagreement % | Questions where judges differ by >15 points |

## Common Commands

```bash
# Evaluate gpt-3.5-turbo on sample
python3 scripts/evaluate_model.py --model gpt-3.5-turbo --output results

# Evaluate on full 900-question benchmark  
python3 scripts/evaluate_model.py --model gpt-4 \
  --questions ../data/questions/cttaf_questions_full_900.csv \
  --output results

# Resume interrupted evaluation
python3 scripts/evaluate_model.py --model gpt-4 --output results
# (automatically skips completed questions)

# Run custom models
python3 scripts/evaluate_model.py --model claude-3-opus --output results
python3 scripts/evaluate_model.py --model gpt-4-turbo --output results
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing API keys" | Edit `.env` with `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` |
| Slow evaluation | Add `--max-questions 10` for quick test |
| Import errors | Run `pip3 install -r requirements.txt` again |
| Interrupted eval | Re-run same command to resume from checkpoint |

## Costs

- **100 questions**: ~$1
- **900 questions**: ~$8-10
- Includes dual-judge scoring (OpenAI + Anthropic)

## Full Documentation

See `BENCHMARK_GUIDE.md` for comprehensive documentation.
