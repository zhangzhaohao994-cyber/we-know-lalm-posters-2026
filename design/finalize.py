from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile,hashlib
P=Path(__file__).resolve().parent.parent
Image.MAX_IMAGE_PIXELS=100_000_000
m=json.loads((P/'manifest.json').read_text());items=m['posters']
locales=json.loads((P/'content/localizations.json').read_text())['languages']
matrix={r['id']:r for r in json.loads((P/'design/matrix.json').read_text())}
for r in items:
 if r['id']=='ORIGINAL':continue
 r['title']=r['id'];r['typography']=matrix[r['id']]['typography']
 if r['id'][:2] in locales:
  r['status']='全页本地化 · 待参与者／母语核对';r['verification']='全页正文、名单与主题按目标语言排版；原文身份保留，未作母语者审校'
  r['concept']=matrix[r['id']]['concept']
m['revision']='4 — Fu Art Coliving added to all posters'
m['notes']=['已确认版补录后仍在第一；日文、韩文、印地语六款随后，中英文版本依编号排列。','外文新稿主题与普通文案整页本地化；专名按原名读音拟写，新增译文待本人／母语核对。','中文十款使用不同真实字体家族与正文搭配；首页十语，桌面手机均单列。','印地语由用户指定，不据此推断参与者母语。','新稿PNG从矢量文字与图形直接导出；网点意象为原创生成图再设计，不是现场纪实照片。']
m['downloads']=[{'label':'26款新稿高清PNG合集','url':'downloads/26-posters-print.zip'},{'label':'可编辑源文件与资料','url':'downloads/design-notes.zip'},{'label':'27张总览','url':'gallery-overview.jpg'}]
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
fonts=ImageFont.truetype(str(P/'fonts/NotoSansCJKsc-Regular.otf'),22)
sheet=Image.new('RGB',(1800,9*940),'#e9e8e3');d=ImageDraw.Draw(sheet)
for i,r in enumerate(items):
 im=Image.open(P/r['preview']).convert('RGB');im.thumbnail((570,855));x=(i%3)*600+15;y=(i//3)*940+50;sheet.paste(im,(x,y));d.text((x,y-35),r['id'],font=fonts,fill='#222')
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
  if r['id'][:2] in locales:
   loc=locales[r['id'][:2]]
   for item in loc['details']:
    if item['text']:assert item['text'] in alltext,(r['id'],item['text'])
   for row in loc['roster']:
    for key in ['project','name']:assert row[key] in alltext,(r['id'],row[key])
   main=''.join(t['text'] for t in texts if not t.get('module')).replace(' ','')
   assert loc['title'].replace(' ','').upper() in main.upper(),(r['id'],'theme missing')
  else:
   for row in rows:
    for v in [row['zh'],row['en'][0],*row['name']]:assert v in alltext,(r['id'],v)
  assert (P/r['source']).read_text().count('<image ')==5
 report.append({'id':r['id'],'dimensions':im.size,'dpi':im.info.get('dpi'),'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(P/'qa/exports.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
quality=P/'QUALITY.md'
base=quality.read_text().split('\n## 本轮成品验收\n')[0]
quality.write_text(base+'\n## 本轮成品验收\n\n26 张新稿均通过 7087×10630、300 PPI、ICC 配置与完整文案检查；每张五份 logo。`qa/exports.json` 记录文件哈希。`qa/layout-r3.json` 验证信息模块内字形边界无相交，原版 GIF 已补入重力体／林中飞，动效保持原参数。\n\n中文十款和日韩四款已逐张看预览；英文十款已看联系页，另有五张外文预览独立检查。日文竖排小假名和印地语组合字形已检查；英文曲引号改用拉丁字体后复看通过。详见本轮补录验收记录。新增译文仍待本人／母语核对。\n\n在线发布与下载验收结果另见当前 STATUS.md 及线上 QA 记录。\n')
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
