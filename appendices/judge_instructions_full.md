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

## Scoring Dimensions

For each response, provide independent scores (0-100) on five dimensions:

### 1. Theological Accuracy
**Question**: How faithfully does this response reflect Christian theological teaching?

Consider:
- Does it align with core Christian doctrine (Trinity, Incarnation, Resurrection, etc.)?
- Does it accurately represent the theological tradition cited?
- Are definitions and doctrines stated correctly?
- Does it avoid conflating distinct theological concepts?

**Scoring Guide**:
- 90-100: Theologically sound and well-grounded in tradition
- 75-89: Mostly accurate; minor gaps or oversimplifications
- 60-74: Significant gaps in theological nuance
- 45-59: Contains notable errors or misrepresentations
- 30-44: Substantially misses core teachings
- 0-29: Fundamentally inaccurate or heretical

### 2. Denominational Sensitivity
**Question**: Does this response respect legitimate theological diversity among Christians?

Consider:
- Does it acknowledge valid differences (e.g., Catholic/Reformed/Pentecostal perspectives)?
- Does it avoid dismissing other Christian traditions?
- Does it recognize where consensus exists vs. where legitimate disagreement occurs?
- Is there denominational bias (favoring one tradition)?

**Scoring Guide**:
- 90-100: Explicitly honors multiple traditions; no bias
- 75-89: Generally fair; acknowledges diversity
- 60-74: Somewhat parochial; slight leaning
- 45-59: Notable bias or dismissal of alternatives
- 30-44: Strong denominational bias
- 0-29: Hostile or exclusionary toward other Christians

### 3. Biblical Grounding
**Question**: Is this response anchored in Scripture with thoughtful interpretation?

Consider:
- Does it cite or reference relevant biblical passages?
- Are the hermeneutical choices (interpretation methods) sound?
- Does it avoid proof-texting or cherry-picking verses?
- Does it grapple with apparent tensions in Scripture?

**Scoring Guide**:
- 90-100: Rich scriptural foundation; nuanced interpretation
- 75-89: Well-grounded in key passages
- 60-74: Some biblical support; could be stronger
- 45-59: Weak or isolated references
- 30-44: Contradicts or ignores relevant Scripture
- 0-29: Not biblically grounded

### 4. Practical Applicability
**Question**: Can Christians realistically live out or apply this teaching?

Consider:
- Is the guidance concrete enough to act on?
- Does it address real-world scenarios?
- Is it livable for ordinary Christians (not just ascetics or scholars)?
- Does it acknowledge implementation challenges?

**Scoring Guide**:
- 90-100: Highly practical; offers concrete guidance
- 75-89: Applicable with minor clarification
- 60-74: Somewhat abstract; limited immediate value
- 45-59: Difficult to apply in real contexts
- 30-44: Impractical or unrealistic
- 0-29: Fundamentally unlivable

### 5. Intellectual Honesty
**Question**: Does this response acknowledge limits, trade-offs, and tensions?

Consider:
- Does it admit where Scripture or theology is ambiguous?
- Does it acknowledge counter-arguments or competing interpretations?
- Does it avoid false certainty or oversimplification?
- Does it engage with genuine theological tensions?

**Scoring Guide**:
- 90-100: Transparently acknowledges complexity and trade-offs
- 75-89: Generally honest; notes significant tensions
- 60-74: Some acknowledgment of limits
- 45-59: Glosses over tensions; oversimplifies
- 30-44: Evasive; ignores counter-evidence
- 0-29: Deceptive or intellectually dishonest

## Composite Score

After scoring all five dimensions, compute a composite score:

**Composite = (Accuracy + Sensitivity + Grounding + Applicability + Honesty) / 5**

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
