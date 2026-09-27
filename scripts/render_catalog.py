"""Render year-grouped domain pages from the current catalog using only stdlib."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = {
    "Architecture": ("architecture", "Interfaces, discrete representations, structured and graph-based representations, attention, and expert routing."),
    "Objective Functions": ("objective-functions", "Contrastive and distributional objectives, reconstruction, grounding constraints, instruction losses, preferences, and verifiable rewards."),
    "Data Construction": ("data-construction", "Paired evidence, local and temporal annotations, synthetic targets, preferences, negatives, and bias controls."),
    "Training": ("training", "Pretraining, instruction tuning, preference and reward optimization, and inference-time interventions."),
    "Evaluation": ("evaluation", "Representation-, task-, and behavior-level evaluation; grounding, robustness, calibration, reward judges, and controlled protocols."),
    "Applications": ("applications", "Embodied systems, safety, healthcare, recommendation, and climate decision support."),
}
ROLES = (
    ("chapter-discussed work", "Studies, Methods, Datasets, and Benchmarks", "studies"),
    ("cross-cutting background", "Related Surveys and Cross-Cutting Background", "background"),
    ("future-direction example", "Future-Direction Examples", "future"),
)


def cell(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", " ").replace("[", "&#91;").replace("]", "&#93;")


def venue_label(venue):
    """Shorten standard venue names, preserving workshop and Findings distinctions."""
    value = venue.lower()
    if "workshop" in value:
        return venue
    if value.startswith("findings of"):
        match = re.search(r"\b(naacl|emnlp|acl)\b", value)
        return "Findings of " + match[1].upper() if match else venue
    if value.startswith("arxiv preprint"):
        return "arXiv"
    patterns = (
        ("neural information processing systems", "NeurIPS"),
        ("computer vision and pattern recognition", "CVPR"),
        ("international conference on computer vision", "ICCV"),
        ("conference on learning representations", "ICLR"),
        ("conference on machine learning", "ICML"),
        ("empirical methods in natural language processing", "EMNLP"),
        ("nations of the americas chapter", "NAACL"),
        ("european chapter of the association", "EACL"),
        ("annual meeting of the association for computational linguistics", "ACL"),
        ("conference on robot learning", "CoRL"),
        ("acm international conference on multimedia", "ACM MM"),
        ("international journal of computer vision", "IJCV"),
        ("transactions on pattern analysis and machine intelligence", "TPAMI"),
        ("transactions on machine learning research", "TMLR"),
    )
    for pattern, label in patterns:
        if pattern in value:
            return label
    if "european conference on computer vision" in value or "eccv" in value:
        return "ECCV"
    if "sigir" in value:
        return "SIGIR"
    return venue or "Not recorded"


def paper_row(paper, domain):
    title = cell(paper["title"])
    work = f"[{title}]({paper['url']})" if paper["url"] else title
    if paper["name"]:
        work = f"**{cell(paper['name'])}**<br>{work}"
    placement = []
    if domain in paper["body_domains"]:
        placement.append("Chapter")
    if paper["timeline_domain"] == domain:
        placement.append("Timeline")
    if not placement:
        placement.append("Future direction" if paper["catalog_role"] == "future-direction example" else "Context mapping")
    return f"| {work} | {cell(venue_label(paper['venue']))} | {', '.join(placement)} | `{paper['citation_key']}` |"


def render_domain(papers, domain):
    selected = [p for p in papers if domain in p["domains"]]
    assert all(p["catalog_role"] in {r[0] for r in ROLES} for p in selected)
    assert all(re.fullmatch(r"\d{4}", p["year"]) for p in selected)
    chapter = sum(domain in p["body_domains"] for p in selected)
    timeline = sum(p["timeline_domain"] == domain for p in selected)
    lines = [
        f"# {domain}", "",
        "[Home](../../README.md) | [All papers](../all-papers.md) | [Catalog](../README.md) | [Classification policy](../classification-policy.md)", "",
        DOMAINS[domain][1], "",
        f"**{len(selected)} mapped records | {chapter} chapter-cited | {timeline} in the timeline**", "",
        "Counts overlap. **Chapter** means cited in this chapter; **Timeline** means assigned to this category in the figure. **Context mapping** is background relevance, not evidence of chapter discussion.", "",
        "Years follow the cited publication record, not necessarily the first preprint or conference year. Within a year, entries are alphabetical, not ranked. Venue abbreviations are for display; [full metadata](../papers.json) and [BibTeX](../../bibliography/current.bib) are preserved.", "",
    ]
    groups = []
    for role, heading, prefix in ROLES:
        records = [p for p in selected if p["catalog_role"] == role]
        if records:
            groups.append((heading, prefix, records))
    for heading, prefix, records in groups:
        years = sorted({p["year"] for p in records}, reverse=True)
        navigation = " | ".join(f"[{y}](#{prefix}-{y})" for y in years)
        lines += [f"**{heading}:** {navigation}", ""]
    for heading, prefix, records in groups:
        lines += [f"## {heading}", ""]
        for year in sorted({p["year"] for p in records}, reverse=True):
            entries = sorted((p for p in records if p["year"] == year), key=lambda p: ((p["name"] or p["title"]).casefold(), p["citation_key"]))
            lines += [f'<a id="{prefix}-{year}"></a>', f"### {year}", "", "| Work / paper | Venue | Survey placement | Citation key |", "| --- | --- | --- | --- |"]
            lines += [paper_row(p, domain) for p in entries]
            lines += [""]
        lines += ["[Back to top](#" + domain.lower().replace(" ", "-") + ")", ""]
    lines += ["---", "", "Generated from `catalog/papers.json` by `scripts/render_catalog.py`. Submit evidence-backed corrections through the [contribution workflow](../../CONTRIBUTING.md).", ""]
    return "\n".join(lines)


def generated_pages(papers):
    return {ROOT / "catalog/domains" / f"{slug}.md": render_domain(papers, domain) for domain, (slug, _) in DOMAINS.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed pages differ; do not write files.")
    args = parser.parse_args()
    papers = json.loads((ROOT / "catalog/papers.json").read_text())
    stale = []
    for path, text in generated_pages(papers).items():
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(text)
    if stale:
        parser.exit(1, "Stale generated pages: " + ", ".join(stale) + "\n")
    print(f"{'Checked' if args.check else 'Rendered'} 6 domain pages from {len(papers)} current records.")


if __name__ == "__main__":
    main()
