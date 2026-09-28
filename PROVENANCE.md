# Provenance and Validation

## Source Snapshot

- Exact manuscript commit: [catalog/manifest.json](catalog/manifest.json).
- Export date: 28 September 2026.
- Active body: `introduction.tex`, `RQ2.tex`, `data.tex`, `RQ3.tex`, `evaluation.tex`, `Applications.tex`, `future.tex`, and `Conclusion.tex`.
- `RQ2.tex` contains both Architecture and Objective Functions; it is split by its actual section boundary during classification.
- Source hashes and figure hashes: [catalog/manifest.json](catalog/manifest.json).

Inactive source files, commented citations, unrelated desktop files, manuscript correspondence, personal author-information drafts, credentials, and full-text paper collections are not uploaded.

## Evidence Preserved

Each current paper has a stable citation key, bibliographic fields, source-link provenance, domain memberships, and active body locations. The complete reading list contains 275 entries; the full timeline contains 163 of these; the printed figure selects 70. All 31 supplement references also belong to the current body-cited set. Exact normalized-title and DOI duplicate checks pass for the current records.

Three active manuscript figures are included. The main manuscript was reduced from 27 to 22 compiled pages without removing any of its 275 body citations. IEEE author-list truncation and venue abbreviations reduce bibliography length while complete author metadata remains in BibTeX. The selected timeline retains the river background, six-domain colors, and institution marks while increasing label size. Its editable foreground was checked by native PowerPoint export. The full timeline and its previous editable sources, including the 26 September background-only style correction, remain available.

The five-page independent supplement has four tables. Table S4 records five within-study observations or contrasts from mDPO, VLGuard, and MM1, with original table/figure locations and inference limits. These are published results, not new experiments for this survey. S3 corrects the ordering of architectural and behavioral alignment in the Fang et al. review. The supplement source and cited bibliography subset match the frozen manuscript snapshot.

Timeline institution mappings were recovered from manuscript commit `d369089`, where they were recorded before the later removal of the `submission/` documentation directory. This repository preserves that attribution record without restoring deleted files to the manuscript project. Logo permission remains pending.

## Checks Performed

- Current citation keys match the 275-record JSON, CSV, and BibTeX exports.
- All 70 selected milestones, all 163 complete-timeline keys, and all supplementary-table keys are current body citations.
- Chapter membership, timeline grouping, and context mappings remain separately inspectable.
- Asset paths are repository-relative; required images and logo originals are present.
- The supplied layout renderer runs with the original locally installed fonts and checks text width before export.
- The main manuscript compiles to 22 pages and the supplement to five, with no undefined-reference, undefined-citation, or font-substitution warnings and no overfull boxes. Main-text underfull-box notices remain and were visually reviewed.
- All main-manuscript pages and figure/table placements were visually inspected; numbered equations have explicit cross-references.
- Markdown local links resolve; packaged files are below GitHub's individual-file size limit.
- Workstation paths and credential-like tokens are excluded from repository documentation and metadata.

These are structural and provenance checks, not a new scientific full-text review of 275 papers. Source URLs generally come from earlier verification records; they have not all been re-fetched. The three previously missing links were recovered from the publisher, conference, or author sources listed in the respective catalog entries.

## Known Boundaries

1. **Version names:** AdViP is the formal IJCV name; AdaViP is the earlier-preprint alias for the same key `Lu2025AdaViPAM`. No extra paper is counted.
2. **Cross-category placement:** the figure's single category and a work's body discussion can differ. The catalog exposes both rather than silently pretending they match.
3. **Historical unresolved keys:** 115 archived keys lack recoverable bibliography metadata. They are not counted as identified papers.
4. **Affiliation versus permission:** attribution metadata is not a license to reproduce institutional marks. See [RIGHTS.md](RIGHTS.md).
5. **Publication status:** the manuscript is being prepared for submission. Authors, ORCIDs, and a final paper citation are not invented here.
6. **Page limit:** the 22-page working target is not confirmation of compliance with TPAMI's 20-page Survey guidance. Real author metadata and submission declarations require final author approval and recompilation.
7. **Search coverage:** revision-time verification does not extend the literature-search cutoff to the export date. No unrecorded screening totals or exclusion counts were reconstructed.

## Updating the Resource

When revising the manuscript, preserve citation keys, update `papers.json` and the CSV/BibTeX exports consistently, and record the new source commit. Keep a removed entry in the history ledger rather than counting it as current. Revalidate timeline and table subsets, update hashes after intentional figure changes, and rerun `scripts/validate_catalog.py` before pushing.

The exporter accepts a committed, verified manuscript snapshot:

```bash
python3 scripts/sync_manuscript.py \
  --source /path/to/manuscript \
  --supplement-pdf /path/to/compiled/supplement.pdf \
  --date YYYY-MM-DD
python3 scripts/validate_catalog.py
```

It refreshes body locations, venue formatting, table exports, and hashes while asserting that the current 275-key citation set is unchanged. A later change in scholarly coverage requires deliberately updating that constraint and the historical ledger.
