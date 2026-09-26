"""Rebuild the timeline from a portable layout; never silently substitute fonts."""
import argparse
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--layout', type=Path, default=ROOT / 'figures/timeline/layout.json')
    parser.add_argument('--font-regular', type=Path, required=True)
    parser.add_argument('--font-bold', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/timeline.pdf')
    parser.add_argument('--png', type=Path)
    parser.add_argument('--width', type=int, default=16000)
    args = parser.parse_args()
    for font, path in [('Regular', args.font_regular), ('Bold', args.font_bold)]:
        if not path.is_file():
            parser.error(f'Font does not exist: {path}')
        pdfmetrics.registerFont(TTFont(font, str(path)))
    if not 100 <= args.width <= 16000:
        parser.error('PNG width must be between 100 and 16000 pixels.')
    layout = json.loads(args.layout.read_text())
    root = args.layout.parent
    width, height = layout['W'], layout['H']
    for item in layout['items']:
        if item['type'] == 'text':
            font = 'Bold' if item['bold'] else 'Regular'
            measure = pdfmetrics.stringWidth(item['text'], font, item['size'])
            if measure > item['w'] + 0.5:
                raise ValueError(f"Text overflow with supplied font: {item['text']}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(args.output), pagesize=(width, height), pageCompression=1, invariant=1)
    c.setTitle('From Foundations to Applications')
    c.setAuthor('Multimodal Alignment Survey')
    c.drawImage(str(root / layout['background']), 0, 0, width, height)
    for item in layout['items']:
        x, y, w, h = item['x'], height - item['y'] - item['h'], item['w'], item['h']
        if item['type'] == 'region':
            c.setFillColor(HexColor(item['fill']))
            c.roundRect(x, y, w, h, item['r'], stroke=0, fill=1)
        elif item['type'] == 'circle':
            c.setFillColor(HexColor(item['fill']))
            c.ellipse(x, y, x + w, y + h, stroke=0, fill=1)
        elif item['type'] == 'image':
            c.drawImage(str(root / item['file']), x, y, w, h, mask='auto')
        else:
            font = 'Bold' if item['bold'] else 'Regular'
            size = item['size']
            c.setFont(font, size)
            c.setFillColor(HexColor(item['color']))
            ascent, descent = pdfmetrics.getAscentDescent(font, size)
            baseline = y + (h - ascent - descent) / 2
            if item['align'] == 'center':
                c.drawCentredString(x + w / 2, baseline, item['text'])
            else:
                c.drawString(x, baseline, item['text'])
    c.showPage()
    c.save()
    print(f'PDF written: {args.output}')
    if args.png:
        import pypdfium2 as pdfium
        args.png.parent.mkdir(parents=True, exist_ok=True)
        with pdfium.PdfDocument(args.output) as doc:
            page = doc[0]
            bitmap = page.render(scale=args.width / page.get_width())
            bitmap.to_pil().save(args.png)
            bitmap.close()
            page.close()
        print(f'PNG written: {args.png}')

if __name__ == '__main__':
    main()
