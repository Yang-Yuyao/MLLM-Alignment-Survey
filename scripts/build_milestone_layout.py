"""Derive a readable manuscript selection; preserve the complete timeline."""
import argparse
import copy
import json
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'figures/timeline'

# One or two examples per existing field retain mechanism and domain coverage.
SELECTION = [
    ['MMV', 'ToB'], ['CLIP', 'ALBEF'], ['Visual Genome', 'RxR'],
    ['RefCOCOg', 'MIL-NCE'], ['CoMMA', 'Landmark-RxR'], ['XDC', 'MERLOT'],
    ['CIDEr', 'CHAIR'], ['GLoRIA', 'CoMIR'], ['SpeechT5', 'Flamingo'],
    ['BLIP', 'InstructGPT'], ['GLIP', 'LF-VILA'], ['CoCa'], ['Winoground'],
    ['MGCA'], ['BLIP-2', '4M'], ['SigLIP', 'DPO'], ['DataComp'],
    ['InstructBLIP', 'LLaVA'], ['POPE', 'SugarCrepe'], ['RT-2', 'VoxPoser', 'SayPlan'],
    ['OneLLM', 'AnyGPT'], ['CLIP-DPO', 'mDPO'], ['DFN', 'MetaCLIP'],
    ['MM1', 'VLGuard'], ['HallusionBench'], ['LLM-CXR', 'FETTLE'],
    ['MoT', 'TokenPacker'], ['GRAM', 'GOAL'], ['SPARCL', 'OmniAlign-V'],
    ['Molmo', 'MM-RLHF'], ['SAIL', 'VidHalluc'], ['EarthDial', 'SafeVLA'],
    ['GraphThinker'], ['AdViP'], ['IRIS', 'ARM-Thinker'], ['Molmo2'],
    ['BLEnD-Vis', 'Chart2Code'], ['ACoT-VLA', 'MLLMRec', 'CrisiSense-RAG'],
]

def text_item(text, x, y, w, h, size, name, bold=False, color='#172028'):
    measured = pdfmetrics.stringWidth(text, 'Bold' if bold else 'Regular', size)
    if measured > w + 0.5:
        raise ValueError(f'Text too wide: {name}, {measured:.1f} > {w:.1f}')
    return dict(type='text', text=text, x=x, y=y, w=w, h=h, size=size,
                name=name, bold=bold, color=color, align='center', measured=measured)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--font-regular', type=Path, required=True)
    ap.add_argument('--font-bold', type=Path, required=True)
    args = ap.parse_args()
    for name, path in [('Regular', args.font_regular), ('Bold', args.font_bold)]:
        pdfmetrics.registerFont(TTFont(name, str(path)))
    original = json.loads((SOURCE/'layout.json').read_text())
    papers = json.loads((SOURCE/'content.json').read_text())
    names = {p['name']:p for p in papers}
    catalog = {p['citation_key']:p for p in json.loads((ROOT/'catalog/papers.json').read_text())}
    available = set(catalog)
    for paper in papers:
        paper.setdefault('cited_year', catalog[paper['citation_key']]['year'])
        paper.setdefault('sort_date', str(paper['cited_year']))
    items = original['items']
    groups, preamble, years = [], [], []
    group = None
    for item in items:
        if item['name'].startswith('Year '):
            years.append(copy.deepcopy(item))
        elif item['type'] == 'text' and item['name'].endswith(' heading'):
            group = dict(heading=item, items=[])
            groups.append(group)
        elif group is None:
            preamble.append(copy.deepcopy(item))
        else:
            group['items'].append(item)
    assert len(groups) == len(SELECTION), (len(groups), len(SELECTION))
    for item in preamble:
        legend_x = {'Architecture': 460, 'Objective Functions': 624, 'Data Construction': 846}
        key = item['name'].removesuffix(' legend swatch')
        if key in legend_x:
            item['x'] = legend_x[key] + (42 if item['type'] == 'text' else 0)
        if item['type'] == 'text' and item['name'] != 'Title':
            item['size'] = 19
            item['measured'] = pdfmetrics.stringWidth(item['text'], 'Regular', 19)
            item['w'] = max(item['w'], item['measured']+1)
    layout = dict(W=original['W'], H=original['H'], background=original['background'], items=preamble)
    selected = []
    for group, choices in zip(groups, SELECTION):
        h = group['heading']
        x, top, width = h['x'], h['y']-5, h['w']
        bottom = max(i['y']+i['h'] for i in group['items']) + 5
        height = bottom-top
        choices = sorted(choices, key=lambda n: (names[n]['sort_date'], n))
        for row, name in enumerate(choices):
            paper = copy.deepcopy(names[name])
            assert paper['citation_key'] in available
            assert int(paper['year']) <= 2021 or str(paper['year']) == str(paper['cited_year']), name
            row_height = height/len(choices)
            row_top = top+row*row_height
            label = 'GOAL (Choi)' if name == 'GOAL' else name
            size = 23
            while pdfmetrics.stringWidth(label, 'Regular', size) > width-2 and size > 21:
                size -= .1
            text_height = 1.2*size
            logos = [copy.deepcopy(i) for i in group['items'] if i['type']=='image' and i['name']==name]
            assert {i['org'] for i in logos} == set(paper['logoOrgs']), name
            logo_height = min(27, row_height-text_height-5)
            logo_width_cap = (width-(len(logos)-1)*7)/len(logos)
            for logo in logos:
                factor = min(logo_height/logo['h'], logo_width_cap/logo['w'], 72/logo['w'])
                logo['w'] *= factor
                logo['h'] *= factor
            actual_height = max(l['h'] for l in logos)
            block_height = actual_height+4+text_height
            block_top = row_top+(row_height-block_height)/2
            total_width = sum(l['w'] for l in logos)+7*(len(logos)-1)
            cursor = x+(width-total_width)/2
            for logo in logos:
                logo['x'] = cursor
                logo['y'] = block_top+(actual_height-logo['h'])/2
                layout['items'].append(logo)
                cursor += logo['w']+7
            layout['items'].append(text_item(label,x,block_top+actual_height+4,width,text_height,size,name))
            paper.update(x=x,y=row_top,w=width,h=row_height,font=size,groupCenter=x+width/2,
                         selection_reason='Representative of a mechanism or domain discussed in the manuscript; full catalog retained.')
            selected.append(paper)
    layout['items'].extend(years)
    for item in layout['items']:
        if item['type'] == 'text':
            assert item['measured'] <= item['w']+.5, item['name']
    (SOURCE/'milestones-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
    (SOURCE/'milestones-content.json').write_text(json.dumps(selected,indent=2)+'\n')

    deck = Presentation(SOURCE/'timeline.pptx')
    slide = deck.slides[0]
    for shape in list(slide.shapes):
        shape._element.getparent().remove(shape._element)
    factor = deck.slide_width / layout['W']
    slide.shapes.add_picture(str(SOURCE/layout['background']),0,0,deck.slide_width,deck.slide_height)
    for item in layout['items']:
        x,y,w,h = (round(item[k]*factor) for k in ['x','y','w','h'])
        if item['type']=='image':
            shape = slide.shapes.add_picture(str(SOURCE/item['file']),x,y,w,h)
        else:
            shape = slide.shapes.add_textbox(x,y,w,h)
            frame = shape.text_frame
            frame.clear()
            frame.margin_left=frame.margin_right=frame.margin_top=frame.margin_bottom=0
            frame.vertical_anchor=MSO_ANCHOR.MIDDLE
            frame.word_wrap=False
            paragraph=frame.paragraphs[0]
            paragraph.alignment=PP_ALIGN.CENTER if item['align']=='center' else PP_ALIGN.LEFT
            paragraph.space_before=paragraph.space_after=Pt(0)
            run=paragraph.add_run()
            run.text=item['text']
            run.font.name='Times New Roman'
            run.font.size=Pt(item['size']*factor/12700)
            run.font.bold=item['bold']
            run.font.color.rgb=RGBColor.from_string(item['color'].lstrip('#'))
        shape.name=item['name']
    slide.notes_slide.notes_text_frame.text='Selected manuscript timeline. Complete 163-study timeline retained separately. Generated from milestones-layout.json; all displayed citations occur in the main text.'
    deck.save(SOURCE/'milestones.pptx')
    print(f'{len(selected)} selected studies; label font {min(p["font"] for p in selected):.1f} to 23 layout units.')

if __name__=='__main__':
    main()
