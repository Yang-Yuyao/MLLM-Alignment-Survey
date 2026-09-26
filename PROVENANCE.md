# Provenance and Validation

## Source Snapshot

- Manuscript snapshot: `06f9038598e3b916bf5067819db8057541936a7f`.
- Export date: 26 September 2026.
- Active body: `introduction.tex`, `RQ2.tex`, `data.tex`, `RQ3.tex`, `evaluation.tex`, `Applications.tex`, `future.tex`, and `Conclusion.tex`.
- `RQ2.tex` contains both Architecture and Objective Functions; it is split by its actual section boundary during classification.
- Source hashes and figure hashes: [catalog/manifest.json](catalog/manifest.json).

Inactive source files, commented citations, unrelated desktop files, manuscript correspondence, personal author-information drafts, credentials, and full-text paper collections are not uploaded.

## Evidence Preserved

Each current paper has a stable citation key, bibliographic fields, source-link provenance, domain memberships, and active body locations. The complete reading list contains 275 entries; the timeline contains 163 of these; all 28 supplement references also belong to the current body-cited set. Exact normalized-title and DOI duplicate checks pass for the current records.

Three manuscript figures are included. The existing timeline PDF is byte-identical to the manuscript figure; its high-resolution PNG and editable PPTX come from the corresponding source build. Workstation-only file paths were removed from PPTX speaker notes, with slide drawings and embedded image bytes preserved. The supplement is recompiled from the unchanged manuscript LaTeX source with the cited bibliography subset.

Timeline institution mappings were recovered from manuscript commit `d369089`, where they were recorded before the later removal of the `submission/` documentation directory. This repository preserves that attribution record without restoring deleted files to the manuscript project. Logo permission remains pending.

## Checks Performed

- Current citation keys match the 275-record JSON, CSV, and BibTeX exports.
- All 163 timeline keys and all supplementary-table keys are current body citations.
- Chapter membership, timeline grouping, and context mappings remain separately inspectable.
- Asset paths are repository-relative; required images and logo originals are present.
- The supplied layout renderer runs with the original locally installed fonts and checks text width before export.
- The supplement compiles to four pages with no undefined-reference or undefined-citation warnings.
- Markdown local links resolve; packaged files are below GitHub's individual-file size limit.
- Workstation paths and credential-like tokens are excluded from repository documentation and metadata.

These are structural and provenance checks, not a new scientific full-text review of 275 papers. Source URLs generally come from earlier verification records; they have not all been re-fetched. The three previously missing links were recovered from the publisher, conference, or author sources listed in the respective catalog entries.

## Known Boundaries

1. **Figure label alias:** the preserved timeline says `AdViP`, whereas the catalog and paper title use `AdaViP` for the same key `Lu2025AdaViPAM`. No extra paper is counted.
2. **Cross-category placement:** the figure's single category and a work's body discussion can differ. The catalog exposes both rather than silently pretending they match.
3. **Historical unresolved keys:** 115 archived keys lack recoverable bibliography metadata. They are not counted as identified papers.
4. **Affiliation versus permission:** attribution metadata is not a license to reproduce institutional marks. See [RIGHTS.md](RIGHTS.md).
5. **Publication status:** the manuscript is being prepared for submission. Authors, ORCIDs, and a final paper citation are not invented here.

## Updating the Resource

When revising the manuscript, preserve citation keys, update `papers.json` and the CSV/BibTeX exports consistently, and record the new source commit. Keep a removed entry in the history ledger rather than counting it as current. Revalidate timeline and table subsets, update hashes after intentional figure changes, and rerun `scripts/validate_catalog.py` before pushing.
