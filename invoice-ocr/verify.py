import json
from pathlib import Path
from pypdf import PdfReader
from extract import parse

out=Path(__file__).parent/'outputs'
pdf=PdfReader(out/'scanned-invoices.pdf')
assert len(pdf.pages)==4
assert all(not p.extract_text().strip() for p in pdf.pages), 'Must be image-only PDF'
r=json.loads((out/'extracted.json').read_text())
assert [x['invoice'] for x in r]==['000041','000042','000043','000041']
assert [x['date'] for x in r]==['10/09/2026','11/09/2026','12/09/2026','10/09/2026']
assert [x['supplier'] for x in r]==['Atelier Exemple','Studio Fictif','Bureau Exemple','Atelier Exemple']
assert [x['client_reference'] for x in r]==['001207','001208',None,'001207']
assert [(x['net'],x['vat'],x['gross']) for x in r]==[('125.00','25.00','150.00'),('200.00','40.00','245.00'),('80.00','0.00','80.00'),('125.00','25.00','150.00')]
assert [x['issues'] for x in r]==[[],['total_mismatch'],['missing_or_ambiguous:client_reference'],['duplicate_supplier_invoice']]
assert r[1]['difference']=='5.00'
assert parse('Reference client :\nTotal HT : 80,00')['client_reference'] is None
assert parse('TVA : unreadable')['vat'] is None
assert parse('Facture : 001\nFacture : 002')['invoice'] is None
print('PASS: four image-only pages; all seven extracted fields per page; 3 anomaly cases; missing/invalid/ambiguous parser regressions')
