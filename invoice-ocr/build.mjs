import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const base=new URL('./outputs/',import.meta.url);
const out=new URL('./01a087f4/',base);await fs.mkdir(out,{recursive:true});
const rows=JSON.parse(await fs.readFile(new URL('extracted.json',base),'utf8'));
const wb=Workbook.create(),s=wb.worksheets.add('Factures');
s.showGridLines=false;
s.getRange('A1:L12').format.font={name:'Arial',size:10,color:'#18263B'};
s.getRange('A2').values=[['Factures scannées : extraction OCR']];
s.getRange('A2').format.font={name:'Arial',size:16,bold:true};
s.getRange('A3').values=[['Source : scanned-invoices.pdf, 4 pages fictives. Montants en EUR.']];
s.getRange('A4').values=[['Les alertes OCR sont celles de l’import initial. Vérifier chaque champ sur le scan avant utilisation.']];
s.getRange('A6:L6').values=[['Page','Facture','Date','Fournisseur','Réf. client','HT (EUR)','TVA (EUR)','TTC (EUR)','Écart TTC','Réf. absente','Doublon','Alertes OCR initiales']];
const translations={'total_mismatch':'Total incohérent','missing_or_ambiguous:client_reference':'Référence absente','duplicate_supplier_invoice':'Facture répétée'};
const amt=v=>v===null?null:Number(v);
s.getRange('A7:L10').values=rows.map(r=>{
 const [d,m,y]=r.date.split('/').map(Number);
 return [r.page,r.invoice,new Date(Date.UTC(y,m-1,d)),r.supplier,r.client_reference,amt(r.net),amt(r.vat),amt(r.gross),null,null,null,r.issues.map(x=>translations[x]??x).join(', ')||'Aucune alerte détectée'];
});
for(let r=7;r<=10;r++){
 s.getRange(`I${r}:K${r}`).formulas=[[
 `=IF(COUNT(F${r}:H${r})=3,ROUND(H${r}-F${r}-G${r},2),"Montant absent")`,
 `=IF(E${r}="","Oui","Non")`,
 `=IF(OR(B${r}="",D${r}=""),"Clé absente",IF(COUNTIFS($B$7:B${r},B${r},$D$7:D${r},D${r})>1,"Oui","Non"))`
 ]];
}
s.getRange('B7:B10').setNumberFormat('000000');s.getRange('E7:E10').setNumberFormat('000000');
s.getRange('C7:C10').setNumberFormat('dd/mm/yyyy');s.getRange('F7:I10').setNumberFormat('#,##0.00');
s.getRange('A6:L10').format.rowHeight=30;s.getRange('A6:L10').format.verticalAlignment='center';
s.getRange('A6:L6').format={fill:'#18324A',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center'};
for(const [i,w] of [55,85,105,160,100,95,95,95,120,115,100,190].entries())s.getRangeByIndexes(0,i,12,1).format.columnWidthPx=w;
s.getRange('I7:I10').conditionalFormats.addCustom('=OR(NOT(ISNUMBER(I7)),I7<>0)',{fill:'#FCE4D6',font:{color:'#9C241A'}});
for(const col of ['J','K'])s.getRange(`${col}7:${col}10`).conditionalFormats.addCustom(`=${col}7<>"Non"`,{fill:'#FCE4D6',font:{color:'#9C241A'}});
// Exercise actual recalculation before restoring the source values.
assert.equal(s.getRange('I8').values[0][0],5);
s.getRange('H8').values=[[240]];assert.equal(s.getRange('I8').values[0][0],0);
s.getRange('H8').values=[[null]];assert.equal(s.getRange('I8').values[0][0],'Montant absent');
s.getRange('H8').values=[[245]];
assert.equal(s.getRange('J9').values[0][0],'Oui');
s.getRange('E9').values=[['001209']];assert.equal(s.getRange('J9').values[0][0],'Non');s.getRange('E9').values=[[null]];
assert.equal(s.getRange('K10').values[0][0],'Oui');
s.getRange('B10').values=[['000044']];assert.equal(s.getRange('K10').values[0][0],'Non');s.getRange('B10').values=[['000041']];
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:s.name,range:'I7:K10',maxChars:1500})).ndjson);
const preview=await wb.render({sheetName:s.name,range:'A1:L11',scale:1.5,format:'png'});
await fs.writeFile(new URL('preview.png',out),new Uint8Array(await preview.arrayBuffer()));
await(await SpreadsheetFile.exportXlsx(wb)).save(new URL('factures.xlsx',out).pathname);
console.log('Saved XLSX; input mutations and restoration passed.');
