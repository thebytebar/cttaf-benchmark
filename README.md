# Christian Theological Triage Alignment Framework (CTTAF)

## Overview
The Christian Theological Triage Alignment Framework is a benchmark for evaluating how well AI language models align with Christian theological values and reasoning across diverse doctrinal perspectives.

## Key Features
- **900 theological questions** covering triage levels, doctrinal dimensions, and denominations
- **Dual-judge evaluation** with two independent LLM judges scoring each response
- **Geometric mean scoring** that penalizes extreme disagreement and incomplete answers
- **Pluralistic Christian perspective** evaluating alignment across denominations

## Quick Start

### Prerequisites
- Python 3.9+
- API keys for OpenAI and Anthropic (for running the benchmark)

### Installation
```bash
# Clone the repository
git clone <repository-url> cttaf
cd cttaf

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r evaluation/requirements.txt
```

### Run the Benchmark
```bash
cd evaluation
python evaluate_model.py --model gpt-4 --output results/gpt4_run.json
python aggregate_results.py --results results/gpt4_run.json
```

## Project Structure
```
cttaf/
├── paper/              # Whitepaper and publishing artifacts
├── data/               # Benchmark datasets (900 questions)
├── prompts/            # Judge system prompts
├── rubric/             # Scoring rubric and formulas
├── evaluation/         # Benchmark evaluation scripts
├── appendices/         # Reproducibility artifacts
└── docs/               # Documentation
```

## Dataset

The benchmark includes:
- **cttaf_questions_full_900.csv** - Complete dataset with metadata
- **cttaf_questions_sample_100.csv** - Quick-start sample

Each question includes:
- Theological content
- Triage level (foundational/secondary/tertiary)
- Doctrinal dimension
- Denomination context

## Evaluation Approach

1. **Dual Judges**: Two independent LLM judges score each response
2. **Scoring**: 0-100 scale with tier-weighted penalties
3. **Aggregation**: Geometric mean reconciles judge disagreement
4. **Validation**: Cohen's kappa measures inter-judge agreement

## Citation

If you use this benchmark, please cite:

```bibtex
@article{cttaf2025,
  title={Christian Theological Triage Alignment Framework: A Benchmark for Evaluating LLM Alignment with Christian Values},
  author={[Author Names]},
  year={2025},
  url={https://github.com/[username]/cttaf}
}
```

## License
CC-BY-SA-4.0 (Creative Commons Attribution-ShareAlike 4.0 International)

## Contributing
Contributions from researchers, theologians, and software engineers are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Resources
- [Whitepaper](paper/cttaf_whitepaper.md) *(🚧 In Progress)*
- [Full Rubric](rubric/cttaf_rubric_v1.0.md)
- [How to Run](docs/how_to_run_benchmark.md)
- [Judge Instructions](appendices/judge_instructions_full.md)
