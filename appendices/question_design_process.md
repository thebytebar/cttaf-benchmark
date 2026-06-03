# Appendix: Question Design Process

*This document outlines how theological questions for the CTTAF benchmark are designed, vetted, and added to the dataset.*

## Overview

The CTTAF benchmark contains 732 questions spanning:
- **Triage Levels**: Foundational, Secondary, Tertiary
- **Theological Dimensions**: Christology, Soteriology, Pneumatology, Ecclesiology, Eschatology, Theodicy, Christian Ethics, etc.
- **Denominational Contexts**: Ecumenical, Catholic, Orthodox, Reformed, Wesleyan, Pentecostal, etc.

## Question Design Principles

1. **Theological Rigor**: Questions should probe meaningful aspects of Christian belief and practice, not trivia.

2. **Denominational Fairness**: Questions should be answerable from multiple Christian perspectives, or explicitly frame the denominational context.

3. **Clarity**: Questions should be unambiguous enough for an LLM to interpret correctly.

4. **Scalability**: Questions should admit nuanced answers (not yes/no dichotomies).

5. **Triage Appropriateness**: Questions should genuinely fit their assigned tier.

## Design Workflow (2026 Improvements)

The current question set (cttaf_questions_full.csv) was produced via an improved generator + hand-curation process to address earlier issues of extreme templating, broken anaphora, and shallow scenarios.

### Phase 1: Subtopic & Rank Definition
- Use the classical Mohler/Ortlund triage (Primary/Secondary/Tertiary) mapped to systematic theology loci (see whitepaper Section 2.2).
- Maintain ~16 questions per Primary subtopic, ~13 per Secondary, ~9 per Tertiary for statistical power on gospel essentials while prioritizing quality.

### Phase 2: Diverse Template & Scenario Generation
- 30+ distinct prompt styles (objective probes + rich pastoral scenarios).
- Objective styles include: core teaching, biblical basis + implications, system coherence tests, common misconceptions/corrections, guards-against-heresy probes, and relation to the gospel.
- Pastoral styles are deliberately contextual (new believer, struggling Christian with specific doubt, parent, skeptic objection, church leadership conflict, abuse/theodicy scenarios, cross-rank coherence traps, etc.).
- Natural phrasing per subtopic (e.g., "regarding the hypostatic union" rather than "on Hypostatic Union").

### Phase 3: Adversarial / Precision Injection + Hand Curation
- For Primary (and some Secondary) subtopics, inject targeted probes that surface common LLM failure modes (works-righteousness, softening of deity, "all views are secondary," etc.).
- Hand-curate 10–15 high-precision questions on the most critical gospel loci (Justification by Faith, Deity of Christ, Hypostatic Union, Atonement, Bibliology essentials, Trinity distinctions).

### Phase 4: Triage Audit & Metadata
- Every subtopic receives a `Triage_Notes` field flagging borderline cases (e.g., Gender & Sexuality has Primary elements in creation order/imago Dei/sexual ethics but is carried as Secondary for ecclesial roles per the original framework).
- `Suggested_Triage_Weight` column for future tooling.
- Questions that could allow a Tertiary view to undermine a Primary doctrine are explicitly tested for coherence.

### Phase 5: Validation & Integration
- Generator script in `scripts/generate_cttaf_questions.py` (reproducible, seedable).
- All prompts are self-contained and unique (no "this concept" anaphora).
- Added to `data/questions/cttaf_questions_full.csv` + diverse samples.
- Human review of a subsample for naturalness, theological soundness, and triage fit.

The generator and hand-curated additions directly implement the recommendations from the initial project review (variety, realistic scenarios, precision probes, triage transparency).

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
