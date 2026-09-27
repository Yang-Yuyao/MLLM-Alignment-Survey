"""Validate citation coverage, assets, checksums, and repository-local documentation links."""
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

import bibtexparser
from PIL import Image
from pypdf import PdfReader
from render_catalog import DOMAINS, generated_pages

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT / name).read_text())

def main():
    papers = load('catalog/papers.json')
    manifest = load('catalog/manifest.json')
    ids = {p['citation_key'] for p in papers}
    assert len(ids) == len(papers) == manifest['current_paper_count'] == 275
    for path, expected in generated_pages(papers).items():
        assert path.read_text() == expected, f'Regenerate {path.name} with scripts/render_catalog.py'
    readme = (ROOT / 'README.md').read_text()
    for domain, (slug, _) in DOMAINS.items():
        page = (ROOT / f'catalog/domains/{slug}.md').read_text()
        displayed = re.findall(r'\| `([^`]+)` \|$', page, re.MULTILINE)
        selected = {p['citation_key'] for p in papers if domain in p['domains']}
        assert len(displayed) == len(selected) and set(displayed) == selected, domain
        chapter = sum(domain in p['body_domains'] for p in papers)
        timeline = sum(p['timeline_domain'] == domain for p in papers)
        row = next(line for line in readme.splitlines() if line.startswith(f'| [{domain}]'))
        assert row.endswith(f'| {chapter} | {timeline} |'), domain
        anchors = set(re.findall(r'<a id="([^"]+)"', page)) | {slug}
        assert set(re.findall(r'\]\(#([^)]+)\)', page)) <= anchors, domain
    with (ROOT / 'catalog/papers.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    assert {r['citation_key'] for r in rows} == ids
    bib = bibtexparser.loads((ROOT / 'bibliography/current.bib').read_text())
    assert {e['ID'] for e in bib.entries} == ids
    for p in papers:
        assert p['domains'] and p['body_locations'], p['citation_key']
        if p['url']:
            parsed = urlsplit(p['url'])
            assert parsed.scheme in {'http', 'https'} and parsed.netloc, p['citation_key']
    timeline = load('figures/timeline/content.json')
    timeline_ids = {p['citation_key'] for p in timeline}
    assert len(timeline_ids) == len(timeline) == manifest['timeline_paper_count'] == 163
    assert timeline_ids <= ids
    for table in load('supplement/tables/index.json'):
        assert set(table['citation_keys']) <= ids, table['table']
        assert table['rows'] == 7
    cite = re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]*)\}')
    for tex in (ROOT / 'supplement').rglob('*.tex'):
        citations = {k.strip() for m in cite.finditer(tex.read_text()) for k in m[1].split(',')}
        assert citations <= ids, (tex, citations - ids)
    for field in ['doi', 'title']:
        seen = set()
        for p in papers:
            value = re.sub(r'\W+', '', p[field].lower())
            if value:
                assert value not in seen, (field, value)
                seen.add(value)
    archive = load('catalog/history/inactive-entries.json')
    archive_ids = {p['citation_key'] for p in archive}
    assert len(archive_ids) == len(archive) == manifest['archived_entry_count']
    assert not archive_ids & ids and '' not in archive_ids
    snapshots = load('catalog/history/snapshots.json')
    assert set(snapshots[-1]['citation_keys']) == ids
    assert snapshots[-1]['commit'] == manifest['manuscript_commit']
    layout_root = ROOT / 'figures/timeline'
    layout = load('figures/timeline/layout.json')
    assert (layout_root / layout['background']).is_file()
    for item in layout['items']:
        if item['type'] == 'image':
            assert not Path(item['file']).is_absolute()
            assert (layout_root / item['file']).is_file(), item['file']
        assert item['x'] >= 0 and item['y'] >= 0, item.get('name')
        assert item['x'] + item['w'] <= layout['W'] + 1, item.get('name')
        assert item['y'] + item['h'] <= layout['H'] + 1, item.get('name')
    for entry in load('figures/timeline/logos.json'):
        assert (layout_root / entry['render_asset']).is_file()
        if entry.get('original_asset'):
            assert (layout_root / entry['original_asset']).is_file()
    for name, digest in manifest['figure_hashes'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    Image.MAX_IMAGE_PIXELS = 200_000_000
    with Image.open(ROOT / 'figures/figure-3-timeline-16000.png') as im:
        assert im.width == 16000
    assert len(PdfReader(ROOT / 'figures/figure-3-timeline.pdf').pages) == 1
    assert len(PdfReader(ROOT / 'supplement/supplement.pdf').pages) == 4
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(p in {'.git', 'build', '__pycache__', '.venv'} for p in path.relative_to(ROOT).parts):
            continue
        assert path.stat().st_size < 100 * 1024 * 1024, path
        if path.suffix in {'.md', '.json', '.csv', '.tex', '.bib', '.py'}:
            text = path.read_text()
            non_urls = re.sub(r'https?://[^\s"<>]+', '', text)
            assert not re.search(r'/(?:Users|home)/[A-Za-z0-9_.-]+/', non_urls), path
            assert not re.search(r'gh[pousr]_[A-Za-z0-9]{25,}', text), path
            assert not re.search(r'[\u4e00-\u9fff]', text), path
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if target.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue
                target = unquote(target.split('#')[0])
                assert (path.parent / target).exists(), (path, target)
    with zipfile.ZipFile(layout_root / 'timeline.pptx') as z:
        assert z.testzip() is None
        assert len([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)]) == 1
        for name in z.namelist():
            if name.endswith('.xml'):
                assert b'/Users/' not in z.read(name), name
    print(f'PASS: {len(papers)} current records; {len(timeline)} timeline records; 3 supplementary tables; 3 figures.')
    print(f'PASS: {len(archive)} archived records; {len(snapshots)} history snapshots; all packaged links and assets resolve.')
    print('Boundary: URL reachability, scientific claims, and logo permissions are not certified by these structural checks.')

if __name__ == '__main__':
    main()
