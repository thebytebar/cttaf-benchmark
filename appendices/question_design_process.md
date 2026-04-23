# Appendix: Question Design Process

*This document outlines how theological questions for the CTTAF benchmark are designed, vetted, and added to the dataset.*

## Overview

The CTTAF benchmark contains 900 questions spanning:
- **Triage Levels**: Foundational, Secondary, Tertiary
- **Theological Dimensions**: Christology, Soteriology, Pneumatology, Ecclesiology, Eschatology, Theodicy, Christian Ethics, etc.
- **Denominational Contexts**: Ecumenical, Catholic, Orthodox, Reformed, Wesleyan, Pentecostal, etc.

## Question Design Principles

1. **Theological Rigor**: Questions should probe meaningful aspects of Christian belief and practice, not trivia.

2. **Denominational Fairness**: Questions should be answerable from multiple Christian perspectives, or explicitly frame the denominational context.

3. **Clarity**: Questions should be unambiguous enough for an LLM to interpret correctly.

4. **Scalability**: Questions should admit nuanced answers (not yes/no dichotomies).

5. **Triage Appropriateness**: Questions should genuinely fit their assigned tier.

## Design Workflow

### Phase 1: Brainstorm
- Identify theological topics relevant to AI alignment and Christian values
- Solicit input from theologians, pastors, and Christian ethicists
- Brainstorm 5-10 candidate questions per topic

### Phase 2: Vetting
For each candidate question:
- **Theological accuracy**: Confirm the topic is real and non-trivial
- **Fairness**: Can it be answered faithfully from multiple Christian traditions?
- **Clarity**: Is it interpretable by an LLM?
- **Triage fit**: Does it belong at foundational/secondary/tertiary level?

Questions that fail vetting are revised or rejected.

### Phase 3: Refinement
- Combine similar questions or split overly broad ones
- Add clarifications if ambiguity remains
- Benchmark against related literature on theological AI evaluation

### Phase 4: Metadata
For each approved question, record:
- **Question ID**: Unique identifier (q001, q002, etc.)
- **Question Text**: The actual prompt
- **Tier**: Foundational / Secondary / Tertiary
- **Dimension**: Primary theological dimension
- **Denomination Context**: Ecumenical, or specific tradition(s)
- **Source**: Where the question came from
- **Notes**: Additional guidance for judges (if needed)

### Phase 5: Integration
Questions are added to `data/questions/cttaf_questions_full_900.csv` and tracked in version control.

## Triage Levels Defined

### Foundational
Core Christian doctrine affirmed across denominations:
- The Incarnation (God became human in Jesus)
- The Resurrection (Jesus rose from the dead)
- Salvation through faith in Christ
- The authority of Scripture
- The Trinity

*Expectation*: Any Christian should be able to affirm a correct answer.

### Secondary
Widely held but genuinely debated:
- The nature of atonement (substitutionary vs. christus victor vs. other models)
- Predestination and free will
- The role of works in justification
- Spiritual gifts and their expression today
- The nature of the millennium

*Expectation*: Most Christians would recognize valid answers, but legitimate disagreement exists.

### Tertiary
Denomination-specific or highly contested:
- Infant vs. believer baptism
- Speaking in tongues as evidence of the Holy Spirit
- The nature of the Eucharist / Communion
- Clerical celibacy
- Women in pastoral leadership

*Expectation*: Only one tradition's answer is "correct" for them; other traditions have different but valid answers.

## Dimension Categories

| Dimension | Examples |
|-----------|----------|
| **Christology** | Who is Jesus? Nature of incarnation, resurrection |
| **Soteriology** | How are we saved? Nature of grace, justification, sanctification |
| **Pneumatology** | Role of the Holy Spirit, gifts, indwelling |
| **Ecclesiology** | Nature of the church, authority, sacraments |
| **Eschatology** | End times, millennialism, eternal state |
| **Theodicy** | Problem of evil, suffering, divine providence |
| **Christian Ethics** | Moral reasoning, bioethics, justice, sexuality |
| **Scripture** | Authority, interpretation, inspiration |

## Quality Checks

Before a question enters the benchmark:

1. **Theological Accuracy Review**: At least one theologian verifies content is accurate.
2. **Cross-Tradition Check**: Can it be fairly answered from ≥2 Christian perspectives?
3. **Clarity Audit**: Test with a small LLM sample to ensure comprehension.
4. **Redundancy Check**: Ensure it's not duplicative of existing questions.
5. **Triage Validation**: Confirm it belongs at the assigned level.

## Contributing New Questions

Researchers or theologians wishing to contribute questions should:

1. Follow this design process
2. Provide question text, tier, dimension, and denomination context
3. Include brief rationale for inclusion
4. Run the question by 2-3 reviewers from different traditions
5. Submit a PR with updated CSV and supporting documentation

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

---

*This process ensures the benchmark remains theologically rigorous, fair, and continuously improving.*
