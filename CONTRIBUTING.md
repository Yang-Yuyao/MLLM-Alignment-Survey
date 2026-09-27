# Contributing

This private repository is a companion to a specific manuscript snapshot. Changes should improve its accuracy and usability without silently changing what the manuscript cites.

## Corrections

For a metadata, classification, or comparison-table correction, provide:

- The stable citation key and affected file or table row.
- The proposed correction and a primary source, preferably the publisher, proceedings, paper PDF, or official project page.
- The exact page, section, table, or source passage when the change concerns a scientific claim.
- Whether the correction affects chapter placement, timeline placement, or both. These are separate fields.

Do not infer a paper's publication year from its citation key or arXiv identifier. Preserve method-name capitalization, distinguish papers with the same acronym, and avoid inventing method names or implementation links.

## Proposed Papers

A proposed addition does not become a current citation merely because it is relevant. First establish its relevance to a survey domain and update the manuscript, or keep it clearly separate from the current catalog pending review. Never increase the advertised current count with uncited candidates.

When the manuscript changes, update the JSON, CSV, and BibTeX exports together, preserve citation keys, and record the new source snapshot. Removed citations belong in the historical ledger, with their previous status and source evidence intact. Update count checks intentionally when the snapshot changes; do not weaken them just to make validation pass.

## Documentation and Assets

- Keep repository text in English and link to existing resources using repository-relative paths.
- Generate the six domain pages from `catalog/papers.json`; do not edit their tables by hand.
- Keep the full venue metadata in the catalog even when a generated page uses a standard abbreviation.
- Do not upload third-party paper PDFs, credentials, correspondence, or unconfirmed personal author details.
- Attribution does not establish logo reuse permission. Follow [RIGHTS.md](RIGHTS.md) before changing assets or making the repository public.
- Use references selectively: adapt organizational ideas that help this resource, without copying another project's text, taxonomy, artwork, or irrelevant fields.

## Verification

```bash
python3 -m pip install -r requirements.txt
python3 scripts/render_catalog.py
python3 scripts/render_catalog.py --check
python3 scripts/validate_catalog.py
python3 scripts/catalog_stats.py
```

Check the rendered Markdown for readable tables, working navigation, and correct figure placement. For intentional figure changes, inspect the output and update checksums only after review. Validation checks packaging and citation membership; it does not certify scientific claims, URL availability, or logo permissions.

## Manuscript Citation

A formal citation will be added after the author list and public manuscript record are confirmed. Do not add a placeholder DOI, acceptance badge, or invented publication status.
