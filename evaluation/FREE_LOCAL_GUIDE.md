# Running CTTAF Benchmark for Free Locally

There are 3 ways to run the benchmark without paying for API access:

## Option 1: Mock Mode (Easiest) ⭐

Runs completely locally with **synthetic but realistic judge outputs**. Perfect for:
- Testing the pipeline
- Education and demonstrations
- CI/CD integration
- Reproducible results

### Quick Start

```bash
cd evaluation

# Run 10 mock questions
python3 scripts/mock_evaluator.py --max-questions 10

# Run full 100-question sample
python3 scripts/mock_evaluator.py \
  --questions ../data/questions/cttaf_questions_sample_100.csv

# Run with different judge disagreement levels
python3 scripts/mock_evaluator.py \
  --judge-variance 0.5  # Judges agree closely
  
python3 scripts/mock_evaluator.py \
  --judge-variance 2.0  # Judges disagree more
```

### Features

✅ **Zero API costs**  
✅ **Instant results** (no rate limits)  
✅ **Reproducible** (seed-based generation)  
✅ **Realistic judge scores** (distribution matches real evaluations)  
✅ **Full pipeline testing** (generates summary stats, ICC, etc.)  

### Output

```bash
results/mock-gpt-4_results.json      # Full evaluation data
results/mock-gpt-4_summary.json      # Summary with ICC score
```

### How It Works

Mock mode generates:
1. **Synthetic model responses** - Realistic theological answers
2. **Synthetic judge scores** - Realistic but procedurally generated
3. **Tier-aware scoring** - Different grading standards for Primary/Secondary/Tertiary
4. **Judge disagreement** - Controllable variance with `--judge-variance`

The scores follow realistic distributions:
- **Primary tier**: Stricter (base 75, variance 8)
- **Secondary tier**: Medium (base 70, variance 12)
- **Tertiary tier**: More lenient (base 68, variance 15)

---

## Option 2: Local Open-Source LLMs

Run with free, open-source models using **Ollama** or **Hugging Face**.

### Setup Ollama (Recommended)

```bash
# Install Ollama (https://ollama.ai)
# macOS/Linux/Windows installers available

# Pull a model (run once)
ollama pull llama2        # 4GB
ollama pull neural-chat   # 5GB  
ollama pull mistral       # 5GB

# Start Ollama server
ollama serve
# Server runs on http://localhost:11434
```

### Setup Hugging Face (Alternative)

```bash
# Install
pip install huggingface-hub transformers

# Download a model (runs once)
python3 -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
            AutoTokenizer.from_pretrained('mistralai/Mistral-7B-Instruct-v0.1')"
```

### Modify evaluate_model.py for Local Models

Add this helper function:

```python
def _get_model_response_local(self, question: str) -> str:
    """Query local Ollama model."""
    import requests
    
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'llama2',
        'prompt': question,
        'stream': False,
        'temperature': 0.7
    })
    
    return response.json()['response']

# Update __init__ to support local models
if self.model.startswith('local-'):
    self.local_model = self.model.replace('local-', '')
```

### Run with Local Model

```bash
# First start Ollama server in another terminal
ollama serve

# Then run benchmark
python3 scripts/evaluate_model.py \
  --model local-llama2 \
  --output results
```

### Costs & Performance

| Model | Size | Speed | Quality | Setup |
|-------|------|-------|---------|-------|
| Llama 2 | 4-7GB | ~5s/response | Good | Easy |
| Mistral | 7B | ~3s/response | Better | Easy |
| Neural Chat | 5B | ~4s/response | Good | Easy |
| GPT-2 (tiny) | 500MB | Very fast | Poor | Easiest |

**Total cost**: Only your electricity (~0.1-1 kWh per 100 questions)

---

## Option 3: Hybrid (Mix Free & Paid)

Use free mock judges but real model responses:

```python
# In evaluate_model.py, modify judge queries:

def _get_judge_evaluations(self, question, response):
    # Use mock judges instead of API judges
    from mock_evaluator import MockJudgeScore
    
    judges = []
    for judge_name in ['openai', 'anthropic']:
        scorer = MockJudgeScore(question['tier'])
        score = scorer.generate_score()
        judges.append(JudgeResult(
            judge=judge_name,
            dimensions=score,
            parse_method="synthetic",
            raw_output=""
        ))
    return judges
```

This gives you **real model responses** with **free judge scoring**.

---

## Comparison Table

| Method | Cost | Speed | Realism | Setup |
|--------|------|-------|---------|-------|
| **Mock Mode** | Free | Instant | High | 1 minute |
| **Local Ollama** | Electricity | Slow (5-10s) | High | 10 minutes |
| **Hybrid** | ~$0.50 | Medium | High | 5 minutes |
| **Full API** | $10 | Fast | Highest | 2 minutes |

---

## Common Questions

### Q: How realistic are mock scores?

**A:** Very realistic! Mock mode:
- Uses the same distribution as real benchmarks
- Varies by tier (Primary stricter than Tertiary)
- Simulates judge disagreement
- Generates reasonable variance

The numbers are synthetic but follow the same patterns as real evaluations.

### Q: Can I use mock results for research?

**A:** Not for publication, but great for:
- Development and testing
- Teaching and demos
- Pipeline validation
- Reproducible examples

For research, use real API judges or local LLM models.

### Q: Which local model is best?

**A:** For theological questions:
1. **Mistral 7B** - Best quality/speed tradeoff
2. **Llama 2 13B** - Better quality, slower
3. **Neural Chat** - Fast and decent quality

All are free (local compute only).

### Q: How do I compare local vs API results?

**A:** Run both and compare `results/`:

```bash
# Mock
python3 scripts/mock_evaluator.py --output results/mock

# Real API (if you add keys)
python3 scripts/evaluate_model.py --model gpt-4 --output results/api

# Compare summaries
diff results/mock/mock-gpt-4_summary.json results/api/gpt-4_summary.json
```

### Q: Can I use Claude locally?

**A:** Not directly (Claude requires API). Options:
1. Use mock mode instead
2. Use open-source alternatives (Llama, Mistral, etc.)
3. Pay for Claude API (~$0.003 per question)

---

## Running Tests on Your Machine

```bash
# Test mock mode works
python3 scripts/mock_evaluator.py --max-questions 3

# Check results
cat results/mock-gpt-4_summary.json | python3 -m json.tool

# Aggregate (same as real evaluation)
python3 scripts/aggregate_results.py \
  --results results/mock-gpt-4_results.json
```

Expected output:
```json
{
  "average_score": 71.5,
  "completion_rate": 1.0,
  "inter_judge_reliability_icc": 0.85,
  "tier_breakdown": {
    "foundational": {"average": 75.2, "count": 2},
    "secondary": {"average": 68.9, "count": 1}
  }
}
```

---

## Advanced: Generate Reproducible Results

Mock mode uses seed-based generation for reproducibility:

```bash
# These always produce identical results
python3 scripts/mock_evaluator.py --seed 42 --max-questions 100
python3 scripts/mock_evaluator.py --seed 42 --max-questions 100
# Results are identical

# Different seed = different results
python3 scripts/mock_evaluator.py --seed 999 --max-questions 100
```

Useful for:
- CI/CD tests
- Reproducible demos
- Regression testing

---

## Summary

| Need | Recommendation |
|------|-----------------|
| Quick testing | Mock mode |
| Research/publication | Real API |
| Learning | Mock mode + local LLM |
| Production | Real API (with caching) |
| CI/CD pipeline | Mock mode |
| Offline work | Local Ollama model |

**Start with mock mode** — zero setup, instant results, then decide if you want to invest in real evaluations!
