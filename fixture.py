"""Generate a labelled, synthetic source document. Never uses client data."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle

out = Path(__file__).parent / 'outputs/01a087f4'
rows = [
    ['Reference', 'Description', 'Quantity', 'Amount (USD)', 'Rate'],
    ['000041', 'Standard service', '12', '1,250.50', '7.50%'],
    ['000042', 'Credit adjustment', '1', '(250.50)', '0.00%'],
    ['000043', 'No charge', '0', '0.00', '0.00%'],
    ['000044', 'Pending amount', '3', '', '5.00%'],
    ['000045', 'Small balance', '2', '0.01', '0.25%'],
    ['000046', 'Negative balance', '1', '-10.00', '10.00%'],
    ['000047', 'Large balance', '4', '99,999.99', '100.00%'],
]
c = canvas.Canvas(str(out / 'source.pdf'), pagesize=(720, 420))
c.setTitle('Synthetic table conversion sample')
c.setAuthor('CDRXRX')
c.setFillColor(HexColor('#18263B')); c.setFont('Helvetica-Bold', 19)
c.drawString(36, 378, 'Table conversion sample')
c.setFont('Helvetica', 10)
c.drawString(36, 356, 'Fictitious records for a conversion demonstration. No client data.')
table = Table(rows, colWidths=[94, 198, 80, 150, 126], rowHeights=29)
table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),10),
    ('BACKGROUND',(0,0),(-1,0),HexColor('#18263B')),
    ('TEXTCOLOR',(0,0),(-1,0),HexColor('#FFFFFF')),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('ALIGN',(2,1),(-1,-1),'RIGHT'),('ALIGN',(0,0),(-1,0),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('GRID',(0,0),(-1,-1),0.5,HexColor('#B8C2D0')),
    ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
]))
table.wrapOn(c,648,232); table.drawOn(c,36,100)
c.setFillColor(HexColor('#526276'));c.setFont('Helvetica',9)
c.drawString(36,74,'Blank amount is intentional. References retain six digits.')
c.drawString(36,57,'Source page 1 of 1. Display conventions: decimal point and comma thousands separator.')
c.save()
(out/'expected.json').write_text(json.dumps(rows,indent=2))
