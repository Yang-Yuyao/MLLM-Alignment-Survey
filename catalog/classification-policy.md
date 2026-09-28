# Classification Policy

## Unit and Scope

The unit of the current catalog is a citation key in the active manuscript body. The 275 records have no exact normalized-title or DOI duplicates in this snapshot. This is not a claim that all preprint and proceedings variants have been exhaustively resolved.

The six domains are Architecture, Objective Functions, Data Construction, Training, Evaluation, and Applications. They describe a work's role in the survey, not exclusive scientific identities. Graph augmentation belongs to Architecture in the current organization; application evidence can still motivate that mechanism.

## Membership Evidence

- **Chapter:** the active source contains a citation in that domain's section. `body_locations` preserves the file, line, subsection, and subsubsection without distributing the manuscript prose.
- **Timeline:** the work is assigned to that domain in the complete 163-entry timeline source. The 70-entry printed figure is a subset of that source. The category identifies its visual grouping, not its only possible use.
- **Context mapping:** a related survey, definition paper, or future-direction example cited outside the six chapters is linked to relevant domains. These entries are explicitly labeled; the mapping is not a claim that the domain chapter itself cites that work.

The union of these memberships is `domains`. `body_domains` and `timeline_domain` remain separate so that readers can inspect cross-category use. Membership counts must not be summed as a unique-paper count.

## Supporting Literature

`catalog_role` distinguishes cross-cutting background, future-direction examples, and chapter-discussed work. The last category can include foundational vision-language learning, text-only optimization or evaluation, and adjacent applications. It does not certify that every listed work is a core MLLM alignment method.

Method names are retained from the timeline where available; full titles and stable citation keys disambiguate otherwise unnamed studies. The two GOAL papers have distinct keys and descriptive labels. AdViP is the formal IJCV name; AdaViP is retained as the earlier-preprint alias for the same citation key, not as an additional paper.

## Years and Source Links

`year` in the paper catalog is copied from the current cited bibliography, without guessing corrections. Timeline placement is separately recorded: its `<=2021` bucket includes earlier publications. `cited_year`, `publication_year`, and `sort_date`, when available, preserve the timeline's date basis.

Links are taken from current bibliographic identifiers or previously recorded source-review metadata. `url_basis` states the origin. Live link availability and full-text correctness were not re-audited for all 275 papers during repository creation.
