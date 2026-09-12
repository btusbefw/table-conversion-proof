"""Generate fictional image-only invoice fixtures, separate from extraction."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen.canvas import Canvas

OUT = Path(__file__).parent / 'outputs'
OUT.mkdir(exist_ok=True)
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 32)
rows = [
    ('000041', '10/09/2026', 'Atelier Exemple', '001207', '125,00', '25,00', '150,00'),
    ('000042', '11/09/2026', 'Studio Fictif', '001208', '200,00', '40,00', '245,00'),
    ('000043', '12/09/2026', 'Bureau Exemple', '', '80,00', '0,00', '80,00'),
]
labels = ['Facture', 'Date', 'Fournisseur', 'Reference client', 'Total HT', 'TVA', 'Total TTC']
canvas = Canvas(str(OUT / 'scanned-invoices.pdf'), pagesize=(595,842))
for i, row in enumerate(rows + [rows[0]], 1):
    im = Image.new('RGB', (1240,1754), 'white')
    draw = ImageDraw.Draw(im)
    draw.text((90,90),'DEMONSTRATION - FACTURE FICTIVE',font=font,fill='#18324A')
    draw.line((90,160,1150,160),fill='#18324A',width=3)
    for j,(label,value) in enumerate(zip(labels,row)):
        draw.text((90,240+j*105),f'{label} : {value}',font=font,fill='black')
    draw.text((90,1200),'Donnees inventees. Aucun paiement a effectuer.',font=font,fill='#555555')
    path=OUT/f'scan-{i:02}.png'
    im.save(path)
    canvas.drawImage(str(path),0,0,595,842)
    canvas.showPage()
canvas.save()
