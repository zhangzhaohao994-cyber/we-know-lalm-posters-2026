from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile,hashlib
P=Path(__file__).resolve().parent.parent
Image.MAX_IMAGE_PIXELS=100_000_000
m=json.loads((P/'manifest.json').read_text());items=m['posters']
for r in items:
 if r['id'].startswith('IN'):
  r['status']='印地语拟音 · 待母语确认';r['verification']='用户指定印地语；HarfBuzz塑形，未作母语者审校'
  r['concept']='连续笔势让完整的天城文字在流动中保持读音。' if r['id']=='IN01' else '同一句标题经过重复压印，边界留下细微而可见的差异。'
m['notes']=['已确认原稿第一；日文、韩文、印地语六款随后，中英文版本依编号排列。','新增日文、韩文与印地语主题采用既有We Know的拟音，已检查字体与排字，待母语者确认。','印地语由用户指定，不据此推断参与者母语。','新稿PNG从矢量文字与图形直接导出；网点意象为原创生成图再设计，不是现场纪实照片。']
m['downloads']=[{'label':'26款新稿高清PNG合集','url':'downloads/26-posters-print.zip'},{'label':'可编辑源文件与资料','url':'downloads/design-notes.zip'},{'label':'27张总览','url':'gallery-overview.jpg'}]
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
fonts=ImageFont.truetype(str(P/'fonts/NotoSansCJKsc-Regular.otf'),22)
sheet=Image.new('RGB',(1800,9*940),'#e9e8e3');d=ImageDraw.Draw(sheet)
for i,r in enumerate(items):
 im=Image.open(P/r['preview']).convert('RGB');im.thumbnail((570,855));x=(i%3)*600+15;y=(i//3)*940+50;sheet.paste(im,(x,y));d.text((x,y-35),r['id']+' · '+r['title'],font=fonts,fill='#222')
sheet.save(P/'gallery-overview.jpg',quality=93)
# Retain only current final contacts in publishable design files.
for f in (P/'design').glob('contact-*.jpg'):f.unlink()
for part in range(3):sheet.crop((0,part*2820,1800,(part+1)*2820)).save(P/'design'/f'final-contact-{part}.jpg',quality=92)
report=[]
for r in items:
 file=P/r['full'];im=Image.open(file)
 if r['id']!='ORIGINAL':
  assert im.size==(7087,10630),(r['id'],im.size)
  assert abs(im.info.get('dpi',(0,0))[0]-300)<.1
  assert im.info.get('icc_profile'),r['id']
  texts=json.loads((P/'design'/f"{r['id']}.text.json").read_text());alltext='\n'.join(z['text'] for z in texts)
  rows=json.loads((P/'content/final-layout.json').read_text())['rows']
  for row in rows:
   for v in [row['zh'],row['en'][0],*row['name']]:assert v in alltext,(r['id'],v)
  assert (P/r['source']).read_text().count('<image ')==5
 report.append({'id':r['id'],'dimensions':im.size,'dpi':im.info.get('dpi'),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(P/'qa/exports.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(P/'downloads').mkdir(exist_ok=True)
with zipfile.ZipFile(P/'downloads/26-posters-print.zip','w',zipfile.ZIP_DEFLATED,compresslevel=4) as z:
 for r in items:
  if r['id']!='ORIGINAL':z.write(P/r['full'],arcname=Path(r['full']).name)
with zipfile.ZipFile(P/'downloads/design-notes.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for folder in ['sources','content','design','fonts','assets','qa']:
  for f in (P/folder).rglob('*'):
   if f.is_file() and '__pycache__' not in f.parts and 'Variable' not in f.name and not f.name.startswith('final-contact'):z.write(f,arcname=str(f.relative_to(P)))
 for name in ['README.md','LICENSES.md','QUALITY.md','package.json','research/references.json','research/参考研究台账.md','manifest.json']:
  if (P/name).exists():z.write(P/name,arcname=name)
print('Verified',len(items),'items;',sum(r['bytes'] for r in report),'PNG bytes')
