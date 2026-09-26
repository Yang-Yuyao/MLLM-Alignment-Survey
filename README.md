# Alignment in Multimodal Large Language Models

### A survey companion: mechanisms, supervision, and evidence

**275 cited papers · 6 research domains · 3 manuscript figures · reproducible timeline sources**

This repository accompanies *Alignment in Multimodal Large Language Models: A Survey*, a manuscript being prepared for TPAMI submission. It is a research resource, not a claim of acceptance or IEEE endorsement. The initial snapshot follows the manuscript revision of **26 September 2026**.

[Browse papers](catalog/README.md) · [Supplement](supplement/README.md) · [Figures](figures/README.md) · [Timeline sources](figures/timeline/README.md) · [Citation history](catalog/history/README.md)

## What Is Multimodal Alignment?

Multimodal alignment is the consistency of a model's representations and observable behavior with **input evidence, task requirements, and human expectations**. An image, a spoken instruction, and a sequence of actions should not merely share similar embeddings: the model must connect the right evidence to the right claim or decision.

We distinguish two diagnostic perspectives:

- **Modality Gap:** failure to establish or use task-relevant correspondence across modalities. Our operational definition includes object binding, temporal correspondence, and evidence-dependent responses. It is broader than geometric separation between modality-specific embeddings.
- **Intent Gap:** behavior that conflicts with a specified goal or constraint, such as moving an object that must remain in place, violating a safety requirement, or expressing unjustified certainty.

These perspectives are complementary, not an exhaustive partition of errors. A model can perceive a scene correctly but act inappropriately, or behave cautiously while using incorrect evidence. A reasoning error after correct perception requires further diagnosis; it should not automatically be assigned to either gap.

<p align="center"><img src="figures/figure-2-two-gaps.png" width="620" alt="Four cases separate perception of a blue mug from compliance with the instruction not to move it"></p>

*Figure 2. Perceptual correctness and action compliance are assessed separately for the same scene and instruction. Passing these two checks does not establish general model reliability.*

## Why Does Alignment Matter?

A fluent answer can still be unsupported by an image, inconsistent with a video, or unsuitable for the user's task. Misalignment can produce object hallucinations, incorrect event ordering, failures under modality shifts, unsafe responses, and actions that violate constraints. In medical, robotic, and climate-support settings, an unsupported output can also undermine traceability and downstream decision quality.

Consequently, good benchmark accuracy, similar embeddings, or polished language is not sufficient evidence of alignment. Evaluation must distinguish **what information is available**, **whether the model uses it**, and **whether its behavior meets the stated requirements**.

## How Is Alignment Studied?

The survey connects architectural information access, training signals, update procedures, and evaluation. The domains below are organizational perspectives, not six mutually exclusive method types.

| Domain | Central question | What the catalog covers |
| --- | --- | --- |
| [Architecture](catalog/domains/architecture.md) | What evidence can reach the language model? | Interfaces, discrete representations, structured and graph-based representations, attention, and expert routing. |
| [Objective Functions](catalog/domains/objective-functions.md) | What is optimized? | Contrastive and distributional objectives, reconstruction, grounding constraints, instruction losses, preferences, and verifiable rewards. |
| [Data Construction](catalog/domains/data-construction.md) | Where does supervision come from? | Paired evidence, local and temporal annotations, synthetic targets, preferences, negatives, and bias controls. |
| [Training](catalog/domains/training.md) | Which components are updated, and when? | Pretraining, instruction tuning, preference and reward optimization, and inference-time interventions. |
| [Evaluation](catalog/domains/evaluation.md) | What evidence supports an alignment claim? | Representation-, task-, and behavior-level evaluation; grounding, robustness, calibration, reward judges, and controlled protocols. |
| [Applications](catalog/domains/applications.md) | Which constraints change across domains? | Embodied systems, safety, healthcare, recommendation, and climate decision support. |

The organizing principle is: **two gaps diagnose problems; six domains organize interventions and assessment; three evaluation levels test the resulting claims**. A preference-learning study may appear in Objectives for its loss, Data for its supervision, and Training for its update procedure. Such overlap is recorded rather than removed.

![Overview of multimodal alignment](figures/figure-1-overview.png)

*Figure 1. Data provides supervision, objectives specify optimization targets, and training controls updates. Architecture enables multimodal information flow; evaluation tests evidence use and behavior and informs refinement.*

## Included Work and Scope

The catalog contains **all 275 references cited in the current manuscript body**, including related surveys, foundational methods, methodological background, and adjacent applications. These supporting references are not all claimed to be core MLLM alignment methods. Domain pages distinguish chapter discussion, timeline placement, and background mappings.

The review is a **structured narrative survey**, not an exhaustive systematic review. Its manuscript reports searches through August 2026, selective updates on 9 September 2026, and targeted verification during revision. GUI agents and generation-side alignment are not comprehensively surveyed. The repository export verifies citation membership and packaging; it does not constitute a new full-text review of every source.

- [Complete readable catalog](catalog/all-papers.md): one record per current citation key.
- [CSV](catalog/papers.csv), [JSON](catalog/papers.json), and [BibTeX](bibliography/current.bib): bibliographic metadata, links, domain memberships, and manuscript locations.
- [Classification policy](catalog/classification-policy.md): how chapter membership and timeline categories are kept distinct.
- [Citation history](catalog/history/README.md): preserved historical and inactive entries, with explicit status rather than silently deleting records.

## Historical Timeline

![From Foundations to Applications: timeline of representative work](figures/figure-3-timeline-preview.png)

*Figure 3. A timeline of 163 representative works across six research domains. Colors indicate the organizing category; placement depicts historical development, not a hierarchy or performance ranking. The earliest bucket includes work published before 2021.*

[Vector-text PDF](figures/figure-3-timeline.pdf) · [16,000-pixel PNG](figures/figure-3-timeline-16000.png) · [Editable PPTX](figures/timeline/timeline.pptx) · [Layout, assets, and renderer](figures/timeline/README.md)

The river and colored background are raster artwork; text and foreground elements remain individually editable in the PPTX. Institutional attribution and logo reuse permission are separate issues. See [rights and attribution](RIGHTS.md) before public release.

## Supplementary Comparisons

The supplement provides analytical comparisons, not new experiments or a matched model leaderboard:

1. [Architectural interventions](supplement/tables/architecture-comparison.md): selection mechanisms, supervision assumptions, and appropriate controls.
2. [Operational diagnostic matrix](supplement/tables/diagnostic-matrix.md): evidence failures, constraint violations, and reasoning-capability errors.
3. [Related-survey coverage](supplement/tables/related-survey-coverage.md): version-specific source locations supporting fair comparison with earlier reviews.

The [supplement PDF and LaTeX sources](supplement/README.md) and the six active main-text table sources are included.

## Validate or Rebuild

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_catalog.py

# Inspect counts and status without installing rendering dependencies.
python3 scripts/catalog_stats.py

# Rebuild the timeline with locally licensed font files.
python3 scripts/render_timeline.py \
  --font-regular /path/to/Times-New-Roman.ttf \
  --font-bold /path/to/Times-New-Roman-Bold.ttf \
  --output build/timeline.pdf
```

See [provenance](PROVENANCE.md) for the source snapshot, validation boundaries, and known display-label differences. Author details and a final manuscript citation will be added after author confirmation. No publication license or institutional endorsement is implied.
