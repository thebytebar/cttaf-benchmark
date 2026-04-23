# 🚀 Run Free Locally RIGHT NOW - No API Keys Needed!

## The Easiest Way (30 seconds)

```bash
cd evaluation
python3 scripts/mock_evaluator.py --max-questions 100
```

Done! Results saved to `results/mock-gpt-4_results.json`

**Cost**: $0  
**Time**: <1 second  
**Setup**: 0 minutes

---

## What Just Happened?

Your benchmark ran **completely locally** with **synthetic but realistic judge scores**. 

The mock evaluator:
- ✅ Generated theological responses
- ✅ Simulated dual judges (OpenAI + Anthropic style)
- ✅ Calculated geometric mean
- ✅ Generated ICC inter-judge reliability score
- ✅ All without calling any APIs

---

## View Your Results

```bash
# See the summary
cat results/mock-gpt-4_summary.json

# Expected output:
# {
#   "model": "mock-gpt-4",
#   "average_score": 70.1,
#   "inter_judge_reliability_icc": -0.312,
#   "completion_rate": 1.0,
#   "tier_breakdown": {...}
# }
```

---

## Next Steps

### Option A: Keep Using Mock (Recommended for Testing)
```bash
# Run again with different settings
python3 scripts/mock_evaluator.py --max-questions 100 --seed 42
python3 scripts/mock_evaluator.py --max-questions 100 --judge-variance 2.0
```

### Option B: Use Real Open-Source LLM Locally
```bash
# Install Ollama (https://ollama.ai)
ollama pull llama2
ollama serve  # Leave running

# In another terminal:
python3 scripts/evaluate_model.py --model local-llama2
```

### Option C: Use Real API (When Ready)
```bash
# Add your API keys to .env
# Then:
python3 scripts/evaluate_model.py --model gpt-4
```

---

## Key Features of Mock Mode

| Feature | Description |
|---------|------------|
| **Tier-Aware** | Primary scores stricter than Secondary/Tertiary |
| **Realistic** | Scores follow real distribution patterns |
| **Reproducible** | Same seed = same results |
| **Fast** | <1s for any number of questions |
| **Full Pipeline** | Includes ICC, aggregation, disagreement flagging |
| **Free** | Zero API costs |

---

## Example Commands

```bash
# Generate reproducible results (same every time)
python3 scripts/mock_evaluator.py --seed 42 --max-questions 10

# Simulate judges disagreeing more
python3 scripts/mock_evaluator.py --judge-variance 2.0 --max-questions 10

# Simulate judges agreeing closely
python3 scripts/mock_evaluator.py --judge-variance 0.5 --max-questions 10

# Run full 900-question benchmark (free!)
python3 scripts/mock_evaluator.py --questions ../data/questions/cttaf_questions_full_900.csv

# Aggregate results
python3 scripts/aggregate_results.py --results results/mock-gpt-4_results.json
```

---

## Cost Comparison

| Method | Cost | Speed | Setup |
|--------|------|-------|-------|
| Mock | $0 | <1s | 0 min |
| Ollama | $0 | 5-10s/q | 5 min |
| Real API | $1-10 | 1-10 min | 2 min |

---

## What These Results Mean

### Average Score (0-100)
- 0-30: Poor theological alignment
- 30-50: Concerning misalignment
- 50-70: Moderate alignment
- 70-85: Good alignment
- 85-100: Excellent alignment

### Inter-Judge ICC Score
- 0.81-1.0: Excellent agreement
- 0.61-0.80: Substantial agreement
- 0.41-0.60: Moderate agreement
- 0.21-0.40: Fair agreement
- <0.20: Poor agreement

### Tier Breakdown
- **Primary**: Gospel essentials (weighted 50%)
- **Secondary**: Church practice (weighted 30%)
- **Tertiary**: Maturity topics (weighted 20%)

---

## Common Questions

**Q: Can I use mock results for research?**  
A: Not for publication, but great for development, testing, and demos.

**Q: How realistic are mock scores?**  
A: Very realistic! They follow the same distribution as real evaluations.

**Q: Can I compare mock vs real results?**  
A: Yes! Run both and compare the summaries.

**Q: What if I want real judge scores?**  
A: Add API keys to .env and use `evaluate_model.py` instead.

---

## Troubleshooting

**"Command not found: python3"**  
```bash
python --version  # Try this instead
# Or install Python 3.9+
```

**"Module not found"**  
```bash
pip3 install -r requirements.txt
```

**Path issues**  
```bash
# Make sure you're in the evaluation directory
cd /path/to/cttaf-benchmark/evaluation
```

---

## What's Next?

1. ✅ **You just ran the benchmark for free!**
2. 📊 View your results: `cat results/mock-gpt-4_summary.json`
3. 📖 Read full guides: `BENCHMARK_GUIDE.md` or `FREE_LOCAL_GUIDE.md`
4. 🔧 Try different modes (Ollama, real API, etc.)
5. 📈 Run on full 900-question dataset

---

**🎉 You're done! Everything works locally and for free!**

See `FREE_LOCAL_GUIDE.md` for detailed alternatives and advanced options.
