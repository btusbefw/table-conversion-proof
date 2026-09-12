"""OCR image-only PDFs. Missing/ambiguous fields remain null for review.

Deliberately bounded to the demonstrated French labels; not a universal parser.
"""
import argparse, json, re, subprocess, tempfile
from decimal import Decimal
from pathlib import Path

FIELDS = {'invoice':'Facture','date':'Date','supplier':'Fournisseur',
          'client_reference':'Reference client','net':'Total HT','vat':'TVA','gross':'Total TTC'}

def parse(text):
    result,issues={},[]
    for field,label in FIELDS.items():
        matches=re.findall(r'^'+re.escape(label)+r'[ \t]*:[ \t]*([^\n]*)$',text,re.M|re.I)
        value=matches[0].strip() if len(matches)==1 else None
        if not value:
            result[field]=None
            issues.append('missing_or_ambiguous:'+field)
            continue
        if field in ('net','vat','gross'):
            if not re.fullmatch(r'-?\d+(?:[ .]\d{3})*,\d{2}',value):
                result[field]=None
                issues.append('invalid_amount:'+field)
                continue
            value=Decimal(value.replace(' ','').replace('.','').replace(',','.'))
        result[field]=value
    if all(result[x] is not None for x in ('net','vat','gross')):
        delta=result['gross']-result['net']-result['vat']
        result['difference']=delta
        if delta != 0: issues.append('total_mismatch')
    else: result['difference']=None
    result['issues']=issues
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    records=[];seen=set()
    with tempfile.TemporaryDirectory(prefix='invoice-ocr-') as tmp:
        subprocess.run(['pdftoppm','-r','150','-png',str(a.pdf),str(Path(tmp)/'page')],check=True,capture_output=True)
        for page,image in enumerate(sorted(Path(tmp).glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1])),1):
            text=subprocess.run(['tesseract',str(image),'stdout','-l','fra','--psm','6'],check=True,capture_output=True,text=True).stdout
            (a.output/f'page-{page:02}.txt').write_text(text)
            row=parse(text);row.update(source=a.pdf.name,page=page)
            key=(row['supplier'],row['invoice'])
            if all(key):
                if key in seen: row['issues'].append('duplicate_supplier_invoice')
                seen.add(key)
            records.append(row)
    (a.output/'extracted.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,default=str))
    print(json.dumps({'pages':len(records),'review_pages':sum(bool(r['issues']) for r in records)}))

if __name__=='__main__': main()
