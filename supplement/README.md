# Supplementary Comparisons

[Read the PDF](supplement.pdf) | [LaTeX source](supplement.tex)

The independent supplement compares mechanisms, assumptions, and diagnostic evidence. It reports no new experiments and does not provide a matched model leaderboard.

| Table | Comparison | Reusable formats |
| --- | --- | --- |
| S1 | Architecture: selection mechanisms, assumptions, and controls | [Markdown](tables/architecture-comparison.md), [CSV](tables/architecture-comparison.csv) |
| S2 | Operational diagnostics: evidence failures, constraint violations, and capability errors | [Markdown](tables/diagnostic-matrix.md), [CSV](tables/diagnostic-matrix.csv) |
| S3 | Related-survey coverage: version-specific source locations and interpretation | [Markdown](tables/related-survey-coverage.md), [CSV](tables/related-survey-coverage.csv) |
| S4 | Reported evidence and limits: within-study contrasts in mDPO, VLGuard, and MM1 | [Markdown](tables/reported-evidence.md), [CSV](tables/reported-evidence.csv) |

The Markdown and CSV tables are extracted from the same LaTeX source, with stable citation keys replacing unstable numeric indices. The supplement's 31 distinct references are all present in the current 275-paper body catalog. The five-page supplement also records search/version boundaries. The author line remains pending confirmation; no author identities have been invented.

## Recompile

The directory includes two subset bibliography files and `bibliography-control.bib`, which controls IEEE author-list truncation without deleting complete author metadata. With a LaTeX installation containing `IEEEtran`, `latexmk`, BibTeX, and the listed packages:

```bash
cd supplement
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

The bundled PDF is compiled from the revised manuscript supplement source and the packaged bibliography subset. Table S4 extracts published observations, not new experiments; its source locations and inference limits are explicit.

## Main-Text Tables

`main-text-tables/` also preserves the six active table snippets: survey positioning plus Architecture, Objectives, Data, Training, and Evaluation. `survey_comparison_narrative.tex` is the **inactive narrative alternative**, not a seventh active table. The active survey comparison is `survey_comparison_matrix.tex`.

These snippets use the main manuscript's table colors, column definitions, and citation library; they are not standalone documents. Their referenced papers are covered by `../bibliography/current.bib`.
