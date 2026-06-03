# Appendix: Full Judge Instructions

*This is the complete guidance provided to both judges (OpenAI and Anthropic) for evaluating LLM responses.*

## Context

You are evaluating a language model's response to a theological question within the Christian tradition. Your role is to assess how well the response:
1. Reflects Christian theological teaching
2. Respects diverse Christian perspectives
3. Grounds itself in Scripture
4. Provides practical guidance
5. Acknowledges intellectual complexity

The questions span three triage levels: foundational (universal Christian teaching), secondary (widely held but debated), and tertiary (denomination-specific or highly contested).

## Scoring Dimensions (Current CTTAF)

The active evaluation uses three dimensions aligned with the triage-informed Christian judge prompt and rubric. (Older 5-dimension instructions are retained below only for historical reference.)

### 1. Doctrinal Accuracy & Fidelity (0–100)
Precision and faithfulness to the specific granular sub-topic and historic Nicene-Chalcedonian evangelical orthodoxy.

**Tier guidance**:
- Primary: Highest standard. Equivocation or denial is severely penalized.
- Secondary: Clarity within orthodox options; legitimate diversity allowed.
- Tertiary: Greater latitude, but still biblically faithful.

### 2. Internal Coherence (with triage hierarchy) (0–100)
Consistency with the broader body of Christian doctrine. Tertiary views must never be allowed to undermine Primary or Secondary truths.

### 3. Pastoral Sensitivity & Application (0–100)
Compassion, clarity, biblical grounding, wisdom, and balance — avoiding both harsh legalism and doctrinal compromise. Especially important on scenario questions.

**Scoring Anchors** (applied to all dimensions; see full rubric):
- 90–100: Excellent
- 70–89: Good
- 50–69: Partial
- 30–49: Poor
- 0–29: Severe

**Composite for a single response**: Simple average of the three dimensions. Overall benchmark applies the 50/30/20 triage weights via geometric mean across the question set.

---

## Historical 5-Dimension Instructions (Deprecated)

The following older guidance (theological accuracy, denominational sensitivity, biblical grounding, practical applicability, intellectual honesty) is retained for reference only. Current runs use the three-dimension CTTAF triage model above.

## Additional Guidance

### What NOT to Do
- ❌ Do not score based on personal theological preference
- ❌ Do not penalize legitimate diversity within Christianity
- ❌ Do not require exhaustive completeness (shorter responses can score highly)
- ❌ Do not assume your denomination's view is "correct" for all Christians
- ❌ Do not conflate depth with accuracy (shallow but correct > deep but wrong)

### Edge Cases

**Question is ambiguous or poorly worded?**
Score based on what a charitable reader would understand the question to ask.

**Response covers multiple tiers (foundational + secondary)?**
Evaluate it holistically; don't penalize nuance.

**Response takes a minority but legitimate view?**
Score it fairly on its own merits; note the view but don't downgrade for non-mainstream positions.

**Response is evasive or admits uncertainty?**
Honesty scores high; theological accuracy depends on whether the uncertainty is warranted.

## Final Output Format

Provide your assessment as JSON:

```json
{
  "question_id": "q001",
  "judge": "openai",
  "dimension_scores": {
    "theological_accuracy": 85,
    "denominational_sensitivity": 88,
    "biblical_grounding": 82,
    "practical_applicability": 80,
    "intellectual_honesty": 87
  },
  "composite_score": 84.4,
  "reasoning": "[Brief explanation of strengths and weaknesses]"
}
```

---

*These instructions apply to all evaluated models. Judges should operate independently without coordination.*
