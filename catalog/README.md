# Paper Catalog

The current catalog contains **275 body-cited records**. Bibliography keys are stable identifiers; numerical reference indices are deliberately omitted because they change when the manuscript is edited.

[Home](../README.md) | [Complete list](all-papers.md) | [CSV](papers.csv) | [JSON](papers.json) | [BibTeX](../bibliography/current.bib)

Choose a domain below to browse by publication year, newest first. Each page separates studies from related surveys and cross-cutting background, with year shortcuts and links to the original papers. Years follow the cited publication record; within each year, works are alphabetical rather than ranked.

| Domain | Directory |
| --- | --- |
| Architecture | [Browse](domains/architecture.md) |
| Objective Functions | [Browse](domains/objective-functions.md) |
| Data Construction | [Browse](domains/data-construction.md) |
| Training | [Browse](domains/training.md) |
| Evaluation | [Browse](domains/evaluation.md) |
| Applications | [Browse](domains/applications.md) |

Use the [complete list](all-papers.md) to view each paper exactly once, or download [CSV](papers.csv), [JSON](papers.json), and [BibTeX](../bibliography/current.bib). Authors, year, venue, source link, domain memberships, and exact manuscript citation locations are retained. Where no established short method label was recorded, the full paper title is used instead of inventing an acronym.

Domain counts overlap. `body_domains` records actual chapter citations; `timeline_domain` records the single visual grouping; `domains` combines them with explicitly labeled background mappings. A paper appearing in the timeline is not necessarily explained in the chapter with the same name. See the [classification policy](classification-policy.md).

The [manifest](manifest.json) gives counts and source hashes. The [historical ledger](history/README.md) preserves entries no longer cited, separately from bibliographic candidates that were never observed in the active manuscript.

To correct a record or propose an addition, follow the [contribution workflow](../CONTRIBUTING.md). The six domain pages are generated from `papers.json` with `python3 scripts/render_catalog.py` from the repository root; full metadata is never replaced by display abbreviations.
