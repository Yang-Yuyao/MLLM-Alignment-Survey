"""Refresh catalog locations and supplement exports from an explicit source snapshot."""
import argparse
import copy
import csv
import hashlib
import json
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from pypdf import PdfReader
from render_catalog import DOMAINS, cell, generated_pages

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ['introduction', 'RQ2', 'data', 'RQ3', 'evaluation', 'Applications', 'future', 'Conclusion']
CITE = re.compile(r'\\cite\w*\*?(?:\[[^]]*\])*\{([^}]+)\}')

def cited(text):
    return {k.strip() for m in CITE.finditer(text) for k in m[1].split(',')}

def active(text):
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    return re.sub(r'\\begin\{comment\}.*?\\end\{comment\}', lambda m: '\n'*m[0].count('\n'), text, flags=re.S)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True)+'\n')

def plain(text):
    text = CITE.sub(lambda m: '['+'; '.join(k.strip() for k in m[1].split(','))+']',text)
    text = re.sub(r'\\(?:textbf|emph|textit)\{([^{}]*)\}', r'\1', text)
    text = text.replace('~',' ').replace('\\%','%').replace('\\&','&')
    text = text.replace('$_s$','s').replace('$_i$','i')
    return re.sub(r'\s+',' ',text).strip()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--supplement-pdf',type=Path,required=True)
    ap.add_argument('--date',required=True)
    args = ap.parse_args()
    source = args.source.resolve()
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
    tracked = subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=source,text=True).strip()
    if tracked:
        ap.error('Commit the verified manuscript source before synchronizing its catalog.')
    papers = json.loads((ROOT/'catalog/papers.json').read_text())
    ids = {p['citation_key'] for p in papers}
    locations = defaultdict(list)
    for chapter in CHAPTERS:
        section = subsection = subsubsection = ''
        skipping_float = False
        text = active((source/(chapter+'.tex')).read_text())
        for line_num, line in enumerate(text.splitlines(),1):
            if re.search(r'\\begin\{(?:figure|table)\*?\}',line):
                skipping_float = True
            if re.search(r'\\end\{(?:figure|table)\*?\}',line):
                skipping_float = False
                continue
            if skipping_float:
                continue
            for m in re.finditer(r'\\(section|subsection|subsubsection)\{([^}]+)\}',line):
                if m[1]=='section':
                    section,subsection,subsubsection=m[2],'',''
                elif m[1]=='subsection':
                    subsection,subsubsection=m[2],''
                else:
                    subsubsection=m[2]
            domain=next((d for d in DOMAINS if section.startswith(d)),None)
            for key in cited(line):
                locations[key].append(dict(source_file=chapter+'.tex',line=line_num,section=section,
                                           subsection=subsection,subsubsection=subsubsection,domain=domain))
    assert set(locations)==ids, (sorted(ids-set(locations)),sorted(set(locations)-ids))
    bibliography={}
    libraries={}
    for filename in ['references.bib','data.bib']:
        db=bibtexparser.loads((source/filename).read_text())
        libraries[filename]=db
        for entry in db.entries:
            assert entry['ID'] not in bibliography
            bibliography[entry['ID']]=(filename,entry)
    for p in papers:
        p['body_locations']=locations[p['citation_key']]
        p['body_domains']=[d for d in DOMAINS if any(l['domain']==d for l in p['body_locations'])]
        context=set(p['domains']) if not p['body_domains'] else set()
        p['domains']=[d for d in DOMAINS if d in context or d in p['body_domains'] or d==p['timeline_domain']]
        if p['body_domains']:
            p['catalog_role']='chapter-discussed work'
        filename,entry=bibliography[p['citation_key']]
        p['entry_type']=entry['ENTRYTYPE']
        p['venue']=entry.get('journal',entry.get('booktitle',p['venue']))
        p['bibliography_source']=filename
        if p['citation_key']=='Lu2025AdaViPAM':
            p['name']='AdViP'
            p['aliases']=['AdaViP (earlier preprint)']
    dump(ROOT/'catalog/papers.json',papers)
    csv_path=ROOT/'catalog/papers.csv'
    with csv_path.open(newline='') as f:
        fields=next(csv.reader(f))
    with csv_path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        for p in papers:
            writer.writerow({k:'; '.join(p[k]) if isinstance(p.get(k),list) else p.get(k) for k in fields})
    for path,text in generated_pages(papers).items():
        path.write_text(text)
    lines=['# Complete Paper Catalog','','275 current body-cited records, one row per citation key. Method labels are included where recorded; the exact paper title remains the bibliographic identifier.','','| Key | Work / paper | Year | Domains |','| --- | --- | --- | --- |']
    for p in papers:
        label=(f'**{cell(p["name"])}**<br>' if p['name'] else '')+f'[{cell(p["title"])}]({p["url"]})'
        lines.append(f'| `{p["citation_key"]}` | {label} | {p["year"]} | {", ".join(p["domains"])} |')
    (ROOT/'catalog/all-papers.md').write_text('\n'.join(lines)+'\n')
    writer=BibTexWriter()
    writer.order_entries_by=('ID',)
    db=bibtexparser.bibdatabase.BibDatabase()
    db.entries=[copy.deepcopy(bibliography[k][1]) for k in sorted(ids)]
    (ROOT/'bibliography/current.bib').write_text(writer.write(db))

    supplement=(source/'supplement.tex').read_text()
    supp_ids=cited(active(supplement))
    assert supp_ids<=ids
    shutil.copy2(source/'supplement.tex',ROOT/'supplement/supplement.tex')
    shutil.copy2(source/'bibliography-control.bib',ROOT/'supplement/bibliography-control.bib')
    shutil.copy2(args.supplement_pdf,ROOT/'supplement/supplement.pdf')
    for filename,library in libraries.items():
        db=bibtexparser.bibdatabase.BibDatabase()
        db.entries=[copy.deepcopy(e) for e in library.entries if e['ID'] in supp_ids]
        (ROOT/'supplement'/filename).write_text(writer.write(db))
    for tex in (ROOT/'supplement/main-text-tables').glob('*.tex'):
        shutil.copy2(source/'Tables'/tex.name,tex)
    slugs=['architecture-comparison','diagnostic-matrix','related-survey-coverage','reported-evidence']
    tables=[]
    table_bodies=re.findall(r'\\begin\{table\}\[.*?\\end\{table\}',supplement,re.S)
    assert len(table_bodies)==len(slugs)
    for i,(body,slug) in enumerate(zip(table_bodies,slugs),1):
        header=re.search(r'\\textbf\{.*?\\midrule',body,re.S)[0].removesuffix('\\midrule').removesuffix('\\\\')
        headers=[plain(c) for c in re.split(r'(?<!\\)&',header)]
        rows=[]
        for row in body.split('\\midrule',1)[1].split('\\bottomrule',1)[0].strip().split('\\\\'):
            if row.strip():
                cells=[plain(c) for c in re.split(r'(?<!\\)&',row)]
                assert len(cells)==len(headers),(slug,cells,headers)
                rows.append(cells)
        path=ROOT/'supplement/tables'/slug
        with path.with_suffix('.csv').open('w',newline='') as f:
            csv.writer(f).writerows([headers]+rows)
        caption=plain(re.search(r'\\caption\{([^}]+)\}',body)[1])
        text=[f'# Table S{i}: {caption}','','Source: [supplement.tex](../supplement.tex). Citation keys identify the sources; these are not new experiments.','','| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']
        text+=['| '+' | '.join(c.replace('|','&#124;') for c in row)+' |' for row in rows]
        path.with_suffix('.md').write_text('\n'.join(text)+'\n')
        tables.append(dict(table=f'S{i}',slug=slug,rows=len(rows),citation_keys=sorted(cited(body))))
    dump(ROOT/'supplement/tables/index.json',tables)
    manifest=json.loads((ROOT/'catalog/manifest.json').read_text())
    manifest.update(snapshot_date=args.date,manuscript_commit=commit,supplement_reference_count=len(supp_ids),
                    supplement_tables=tables,supplement_page_count=len(PdfReader(args.supplement_pdf).pages),
                    manuscript_timeline_paper_count=70)
    for name in list(manifest['source_hashes'])+['bibliography-control.bib']:
        manifest['source_hashes'][name]=digest(source/name)
    for name in list(manifest['figure_hashes'])+['figures/figure-3-milestones.pdf','figures/figure-3-milestones-16000.png','figures/figure-3-milestones-preview.png']:
        manifest['figure_hashes'][name]=digest(ROOT/name)
    for domain in DOMAINS:
        manifest['domain_counts'][domain]=dict(total=sum(domain in p['domains'] for p in papers),
            cited_in_chapter=sum(domain in p['body_domains'] for p in papers),timeline=sum(p['timeline_domain']==domain for p in papers))
    snapshots=json.loads((ROOT/'catalog/history/snapshots.json').read_text())
    if snapshots[-1]['commit']!=commit:
        entry=copy.deepcopy(snapshots[-1])
        entry.update(commit=commit,citation_keys=sorted(ids))
        entry['date']=subprocess.check_output(['git','show','-s','--format=%cs','HEAD'],cwd=source,text=True).strip()
        if 'subject' in entry:
            entry['subject']=subprocess.check_output(['git','show','-s','--format=%s','HEAD'],cwd=source,text=True).strip()
        changes_path=ROOT/'catalog/history/changes.csv'
        with changes_path.open(newline='') as f:
            change_fields=next(csv.reader(f))
        assert change_fields==['commit','date','previous_commit','citation_count','added_keys','removed_keys'],change_fields
        previous_ids=set(snapshots[-1]['citation_keys'])
        with changes_path.open('a',newline='') as f:
            csv.writer(f).writerow([commit,entry['date'],snapshots[-1]['commit'],len(ids),
                                   '; '.join(sorted(ids-previous_ids)),'; '.join(sorted(previous_ids-ids))])
        snapshots.append(entry)
    manifest['history_snapshots']=len(snapshots)
    dump(ROOT/'catalog/history/snapshots.json',snapshots)
    dump(ROOT/'catalog/manifest.json',manifest)
    readme=(ROOT/'README.md').read_text()
    for domain,counts in manifest['domain_counts'].items():
        readme=re.sub(r'(\| \['+re.escape(domain)+r'\][^\n]*?\| )\d+ \| \d+ \|',
                      lambda m:m[1]+f'{counts["cited_in_chapter"]} | {counts["timeline"]} |',readme)
    (ROOT/'README.md').write_text(readme)
    history=ROOT/'catalog/history/README.md'
    history.write_text(re.sub(r'- \*\*\d+\*\* tracked Git snapshots[^\n]+',
        f'- **{len(snapshots)}** tracked Git snapshots inspected in ancestry order, ending at manuscript commit `{commit[:7]}` on {args.date}. This revision preserves the current citation set; intermediate layout-only commits are not reconstructed as additional snapshots.',history.read_text()))
    print(f'Synchronized {len(papers)} papers, {len(supp_ids)} supplement citations, and {len(tables)} tables from {commit}.')

if __name__=='__main__':
    main()
