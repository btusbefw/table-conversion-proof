"""Read-only verification of the exported workbook against the PDF fixture."""
import json
from decimal import Decimal
from pathlib import Path
from openpyxl import load_workbook

out = Path(__file__).parent / 'outputs/01a087f4'
expected = json.loads((out / 'expected.json').read_text())
extracted = json.loads((out / 'extracted.json').read_text())
assert len(extracted) == 1 and extracted[0]['page'] == 1
assert extracted[0]['rows'] == expected
wb = load_workbook(out / 'converted.xlsx', data_only=False)
assert wb.sheetnames == ['PDF_p001']
s = wb.active
checked = 0
for r, row in enumerate(expected, start=4):
    for c, source in enumerate(row, start=1):
        cell = s.cell(r, c)
        if r == 4 or c <= 2:
            assert cell.value == source, (cell.coordinate, cell.value, source)
            assert cell.data_type == 's'
        elif source == '':
            assert cell.value is None
        else:
            normalized = source.replace(',', '').replace('(', '-').replace(')', '').replace('%', '')
            target = Decimal(normalized) / (100 if c == 5 else 1)
            assert cell.data_type == 'n', (cell.coordinate, cell.data_type)
            assert Decimal(str(cell.value)) == target, (cell.coordinate, cell.value, target)
        if r > 4:
            if c == 1:
                assert len(cell.value) == 6 and cell.number_format == '000000'
            if c == 5:
                assert cell.number_format == '0.00%'
        checked += 1
assert '(' in s['D6'].number_format
assert s['D7'].value == 0 and s['D8'].value is None
report = {'source_pages': 1, 'cells_verified': checked, 'pdf_extraction_matches_fixture': True,
          'saved_workbook_values_and_types_match': True, 'synthetic_data_only': True}
(out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
