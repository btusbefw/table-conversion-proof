# French invoice OCR demonstration

Independent synthetic proof supporting the invoice-entry proposal for Freelancer project 40707026. No client documents, commission, acceptance or payment.

Four fictional image-only PDF pages are rasterized by Poppler and read locally by Tesseract French OCR. The extractor has no access to the fixture's expected values. It captures invoice number, date, supplier, client reference, net, VAT and gross. Decimal amounts are preserved exactly in JSON as decimal strings. Invoice identifiers remain strings, including initial zeroes.

`verify.py` independently checks that the source PDF has no extractable text and that all seven fields on all four pages match expected values. It also checks three review cases: a 5.00 total mismatch, a missing client reference, and a repeated supplier/invoice. Missing, malformed or multiply matched values remain null. The blank-reference regression originally failed because whitespace matching crossed a newline; the fix uses horizontal whitespace only.

Run with Python containing Pillow, reportlab and pypdf, and installed `pdftoppm` and `tesseract` with French language data:

```sh
python3 fixture.py
python3 extract.py outputs/scanned-invoices.pdf outputs
python3 verify.py
```

Current scope: clean synthetic scans with one controlled layout and explicit French labels. Not evidence of handwriting, low-quality/photo OCR, arbitrary supplier layouts, tax compliance, or a production accuracy rate. Duplicate flags require review and do not delete records. Reconciliation does not prove OCR is correct. All production records need source review and client-approved handling of private files.

Excel export: `outputs/01a087f4/factures.xlsx`, built using `build.mjs` and @oai/artifact-tool. Amounts and dates are typed; references are strings. The three formula columns recalculate amount differences, missing references and repeated supplier/invoice identifiers. Original OCR alerts remain explicitly labeled as the initial extraction snapshot. Input mutation checks cover corrected and missing amounts, reference completion and duplicate removal, then restore every original value. Reopened XLSX types/cached values and rendered appearance were verified. Native Microsoft Excel execution has not been tested.

![Excel output](outputs/01a087f4/preview.png)
