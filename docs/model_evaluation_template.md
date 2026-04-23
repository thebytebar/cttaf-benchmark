# Model Evaluation Template

Use this template when documenting results from a new model evaluation.

## Model Info
- **Model Name**: [e.g., GPT-4, Claude 3 Opus]
- **Version**: [specific version/date]
- **Evaluated Date**: [YYYY-MM-DD]
- **Evaluator**: [name or organization]

## Benchmark Configuration
- **Dataset**: cttaf_questions_full_900.csv (or sample)
- **Judges**: OpenAI (gpt-4) + Anthropic (claude-opus)
- **Scoring Method**: Geometric mean (reconciliation)

## Summary Results

| Metric | Value |
|--------|-------|
| Average Score | [X.X] |
| Median Score | [X.X] |
| Std Dev | [X.X] |
| Min Score | [X.X] |
| Max Score | [X.X] |

## Tier Breakdown

| Tier | Avg Score | Pass Rate (≥70) | Count |
|------|-----------|-----------------|-------|
| Foundational | [X.X] | [X%] | [count] |
| Secondary | [X.X] | [X%] | [count] |
| Tertiary | [X.X] | [X%] | [count] |

## Dimension Scores

| Dimension | Avg | Median | Std Dev |
|-----------|-----|--------|---------|
| Theological Accuracy | [X.X] | [X.X] | [X.X] |
| Denominational Sensitivity | [X.X] | [X.X] | [X.X] |
| Biblical Grounding | [X.X] | [X.X] | [X.X] |
| Practical Applicability | [X.X] | [X.X] | [X.X] |
| Intellectual Honesty | [X.X] | [X.X] | [X.X] |

## Judge Agreement
- **Cohen's Kappa**: [X.XX]
- **Agreement Rate** (within ±5 points): [X%]
- **High Disagreement Cases** (>15 point delta): [count]

## Qualitative Observations

### Strengths
- [e.g., strong on foundational doctrine, good denominational awareness]

### Weaknesses
- [e.g., struggles with practical applicability, oversimplifies tensions]

### Notable Cases
- Best answer: Question [ID] (score: [X])
- Worst answer: Question [ID] (score: [X])
- Most contested: Question [ID] (judge delta: [X] points)

## Recommendations
- [Suggestions for model improvement, fine-tuning, or prompt engineering]

## Reproducibility
- **Date Run**: [YYYY-MM-DD]
- **Results File**: `evaluation/results/example_results/[model_name]_full_results.json`
- **Command**: `python evaluate_model.py --model [name] --output results/[name].json`

---
*For methodology details, see the main whitepaper and rubric documentation.*
