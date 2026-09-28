# Timeline Sources

## Files

- `milestones.pptx`, `milestones-layout.json`, and `milestones-content.json`: the 70-study printed selection, with larger labels and grouped, centered institution marks. The content file records the exact citation-key subset; omitted visual entries remain in the manuscript body and complete timeline.
- `timeline.pptx`: one-slide editable source. Text and logo placements are native objects; the river background is a bitmap. Workstation-local paths in speaker notes were removed during packaging. The 2026 Architecture field received a background-only style correction on 26 September 2026.
- `layout.json`: canvas dimensions and positioned text, image, and region objects. All asset paths are relative to this directory.
- `content.json`: 163 displayed studies, citation keys, categories, year buckets, and grouped logo identifiers.
- `assets/background.png`: the original river and colored-region artwork.
- `assets/markers/`: six highlighter-style legend swatches.
- `assets/logos/`: prepared logo images used by the figure.
- `assets/originals/`: available original logo sources, including vector originals where available.
- `logos.json`: asset formats, dimensions, URLs, and permission status.
- `attribution.json`: paper-level institution mappings and co-first-author interpretation notes from the source revision.

## Editing and Rebuilding

For the manuscript selection, open `milestones.pptx`. Its foreground was also checked by exporting from Microsoft PowerPoint. Rebuild it from the fixed selection in `scripts/build_milestone_layout.py`:

```bash
python3 scripts/build_milestone_layout.py \
  --font-regular /path/to/Times-New-Roman.ttf \
  --font-bold /path/to/Times-New-Roman-Bold.ttf
python3 scripts/render_timeline.py \
  --layout figures/timeline/milestones-layout.json \
  --font-regular /path/to/Times-New-Roman.ttf \
  --font-bold /path/to/Times-New-Roman-Bold.ttf \
  --output build/milestones.pdf \
  --png build/milestones.png --width 16000
```

For manual layout editing, open `timeline.pptx` in PowerPoint. The 2026 Architecture field uses a soft blue background instead of the former flat rounded-rectangle cover. All text, logo assets, and foreground positions are unchanged; the rest of the figure is preserved.

For scripted export, edit `layout.json` and rebuild from the repository root:

```bash
python3 scripts/render_timeline.py \
  --font-regular /path/to/Times-New-Roman.ttf \
  --font-bold /path/to/Times-New-Roman-Bold.ttf \
  --output build/timeline.pdf \
  --png build/timeline.png --width 16000
```

The renderer requires explicitly supplied font files and refuses overflowing text. It does not silently substitute fonts. The original uses Times New Roman regular and bold, which are not redistributed.

The two editing routes are **not automatically synchronized**. A PowerPoint edit does not update `layout.json`; a JSON edit does not update the PPTX. Update both representations when preparing a new archival snapshot. Changing `content.json` alone does not reposition labels.

## Interpretation

The `<=2021` bucket includes earlier foundational papers. Year buckets follow the cited publication versions recorded in the source, not a claim to first-publication priority. Bibliographic and first-release dates may differ; `cited_year`, `publication_year`, and `sort_date` preserve the existing date metadata. Category membership identifies the primary intervention emphasized in the timeline, not a ranking or a claim that a method has only one role. For exact manuscript placement, use `body_locations` in [papers.json](../../catalog/papers.json).

The catalog and figure use the formal IJCV name **AdViP** for citation key `Lu2025AdaViPAM`; **AdaViP** is its earlier-preprint alias. The two papers named GOAL remain disambiguated by citation keys and titles; the selected figure labels the global--local object method `GOAL (Choi)`.

Institutional attribution does not establish reproduction permission. See [RIGHTS.md](../../RIGHTS.md) before reusing the assets.
