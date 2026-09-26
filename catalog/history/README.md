# Citation History and Inactive Records

This directory answers a narrower, verifiable question: **which citation keys occurred in the tracked manuscript, and which are absent from the current version?** It does not infer why a reference was removed, nor equate every old key with a distinct valid paper.

## Current Snapshot

- **275** distinct current body-cited records.
- **417** entries in the current source bibliography library, of which **142** are not currently body-cited.
- **76** tracked Git snapshots inspected in ancestry order, ending at manuscript commit `06f9038` on 26 September 2026.
- **297** historical or library-only records outside the current 275: **279** citation keys observed in an earlier active manuscript and **18** library entries with no active citation observed in the inspected history.
- **115** of those historical keys have no bibliographic metadata recoverable from the tracked bibliography files. They are preserved as unresolved records, not identified papers.

The historical total is larger than the 142 unused entries in today's library because some old keys also disappeared from the library. Keys can additionally be aliases or earlier placeholders. These figures must not be added to 275 as a count of distinct surveyed papers.

## Files

| File | Purpose |
| --- | --- |
| [Readable archive](inactive-entries.md) | Titles where recoverable, status, last observed date, and possible current aliases. |
| [CSV ledger](inactive-entries.csv) / [JSON ledger](inactive-entries.json) | Stable keys, first and last observed commits, and metadata availability. |
| [Per-revision changes](changes.csv) | Keys added or removed between consecutive inspected snapshots. |
| [Snapshot records](snapshots.json) | Active include paths and citation-key sets for each revision. No full manuscript prose. |
| [Archived BibTeX](../../bibliography/archive.bib) | Recoverable bibliographic entries outside the current catalog. Unresolved keys are not fabricated into BibTeX records. |

## Interpretation Rules

`historically_cited_not_current` means that the key was found in an active include chain in at least one earlier snapshot. `library_only_no_active_citation_observed` means no such occurrence was found within the available history. Neither label implies a scientific-quality judgment.

`possible_current_aliases` uses exact normalized titles or matching DOIs. It is a candidate identity link, not proof that a reference was deliberately replaced. Empty alias fields mean that no match was established, not that no match exists.

Historical extraction follows `main.tex` and active `input`/`include` statements, excluding line comments and `comment` environments. Historical tables are included. It is a source-level inventory, not a recompile of every old revision or a complete TeX interpreter; unresolved citations in old drafts can therefore appear. Dates are Git commit dates and are not a reliable ordering when clocks or time zones differ; ancestry order is used instead.

The current 275 records are separately checked against body citations and all packaged timeline and supplementary-table keys. The archive remains outside the active reading list and is not used to inflate survey coverage.
