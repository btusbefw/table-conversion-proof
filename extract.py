"""Extract ruled text-PDF tables. Keep cell text unchanged and page provenance."""
import json
from pathlib import Path
import pdfplumber
root=Path(__file__).parent/'outputs/01a087f4'
with pdfplumber.open(root/'source.pdf') as pdf:
    tables=[{'page':i+1,'rows':t} for i,p in enumerate(pdf.pages) for t in p.extract_tables()]
if len(tables)!=1:
    raise ValueError(f'Expected one table, found {len(tables)}')
(root/'extracted.json').write_text(json.dumps(tables,indent=2))
expected=json.loads((root/'expected.json').read_text())
assert tables[0]['rows']==expected, 'Source extraction differs from independent fixture'
print('All 40 source cells match, including the blank cell.')
