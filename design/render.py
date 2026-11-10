from pathlib import Path
import json,math,random,base64,html,sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageChops
from devanagari_shape import shaped_paths,shaped_width,shape_run
R=Path(__file__).resolve().parent.parent
DATA=json.loads((R/'content/final-layout.json').read_text())
ROWS=DATA['rows'];AS=R/'assets'
LOCALES=json.loads((R/'content/localizations.json').read_text())['languages'] if (R/'content/localizations.json').exists() else {}
F={}
for k,n in [('reg','NotoSansCJKsc-Regular.otf'),('bold','NotoSansCJKsc-Bold.otf'),('jp','NotoSansCJKjp-Bold.otf'),('ko','NotoSansCJKkr-Bold.otf'),('cond','Anton-Regular.ttf'),('wide','ArchivoBlack-Regular.ttf'),('latin','NotoSans-Regular.ttf'),('serif','BodoniModa-Regular.ttf')]:
 f=TTFont(R/'fonts'/n);F[k]=(f,f.getBestCmap(),f.getGlyphSet(),f['head'].unitsPerEm)
f,cm,gs,up=F['jp'];vmap={}
for rec in f['GSUB'].table.FeatureList.FeatureRecord:
 if rec.FeatureTag=='vert':
  for ix in rec.Feature.LookupListIndex:
   for st in f['GSUB'].table.LookupList.Lookup[ix].SubTable:
    vmap.update(getattr(st,'mapping',{}))
F['jpv']=(f,{cp:vmap.get(g,g) for cp,g in cm.items()},gs,up)
EXTRA_FONTS={'song':'LALM-NotoSerifSC-Regular.ttf','songBold':'LALM-NotoSerifSC-Bold.ttf','wenkai':'LALM-WenKai-Regular.ttf','brush':'LALM-MaShanZheng-Regular.ttf','xiaowei':'LALM-XiaoWei-Regular.ttf','qing':'LALM-QingKeHuangYou-Regular.ttf','jpSerif':'LALM-NotoSerifJP-Regular.ttf','jpSerifBold':'LALM-NotoSerifJP-Bold.ttf','koSerif':'LALM-NotoSerifKR-Regular.ttf','koSerifBold':'LALM-NotoSerifKR-Bold.ttf'}
EXTRA_FONTS['latinBold']='NotoSans-Bold.ttf'
for k,n in EXTRA_FONTS.items():
 f=TTFont(R/'fonts'/n);F[k]=(f,f.getBestCmap(),f.getGlyphSet(),f['head'].unitsPerEm)
BODY_FONTS={'ZH01':('song','songBold'),'ZH02':('wenkai','wenkai'),'ZH03':('reg','bold'),'ZH04':('song','songBold'),'ZH05':('wenkai','wenkai'),'ZH06':('song','songBold'),'ZH07':('wenkai','wenkai'),'ZH08':('song','songBold'),'ZH09':('reg','bold'),'ZH10':('wenkai','wenkai')}
BODY_FONTS.update({'JA01':('jpSerif','jp'),'JA02':('jpSerif','jpSerifBold'),'KO01':('koSerif','ko'),'KO02':('koSerif','koSerifBold')})
BODY_FONTS.update({f'EN{i:02}':('latin','latinBold') for i in range(1,11)})
TITLE_FONTS={'ZH01':'songBold','ZH02':'brush','ZH03':'qing','ZH04':'song','ZH05':'xiaowei','ZH06':'bold','ZH07':'wenkai','ZH08':'brush','ZH09':'song','ZH10':'wenkai'}
# Caption fonts are OFL; all final text is outlined to remove runtime font substitutions.
class Art:
 def __init__(self,bg,ink,id):
  self.p=[];self.defs={};self.log=[];self.ink=ink;self.id=id;self.lang=id[:2];self.in_info=False;self.module=None;self.rect(0,0,1200,1800,bg)
 def rect(self,x,y,w,h,c,**kw):self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" '+attrs(kw)+'/>')
 def path(self,d,c='none',stroke=None,sw=1,**kw):self.p.append(f'<path d="{d}" fill="{c}" '+(f'stroke="{stroke}" stroke-width="{sw}" ' if stroke else '')+attrs(kw)+'/>')
 def circle(self,x,y,r,c,**kw):self.p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" '+attrs(kw)+'/>')
 def line(self,x,y,X,Y,c,sw=1):self.path(f'M{x},{y} L{X},{Y}',stroke=c,sw=sw)
 def group(self,t):self.p.append(f'<g transform="{t}">')
 def end(self):self.p.append('</g>')
 def width(self,s,size,font):
  if any('\u0900'<=ch<='\u097f' for ch in s):return shaped_width(s,size,font='Bold' if font in ['bold','hiBold'] else 'Regular')
  return sum(self.charfont(ch,font)[2][self.charfont(ch,font)[1][ord(ch)]].width/self.charfont(ch,font)[3]*size for ch in s)
 def charfont(self,ch,font):
  fallback=['songBold' if 'Bold' in font else 'song'] if 'Serif' in font else []
  for k in [font,*fallback,'latin','reg','jp','ko']:
   if ord(ch) in F[k][1]:return (*F[k],k)
  raise ValueError(f'Missing {ch} in all fonts')
 def text(self,s,x,y,size=18,font='reg',color=None,width=None,rotate=None,opacity=1):
  if not s:return 0
  color=color or self.ink
  if self.in_info and font in ['reg','bold']:
   font=BODY_FONTS.get(self.id,('reg','bold'))[font=='bold']
  if any('\u0900'<=ch<='\u097f' for ch in s):
   weight='Bold' if font in ['bold','hiBold'] else 'Regular';natural=shaped_width(s,size,font=weight)
   if width and natural>width:size*=width/natural
   run=shape_run(s,size,font=weight,x=x,y=y,fill=color)
   self.p.append(f'<g opacity="{opacity}">'+run['svg']+'</g>')
   self.log.append({'text':s,'x':x,'y':y,'size':size,'font':'Devanagari-'+weight,'bbox':run['bbox'],'module':self.module})
   return run['advance_width']
  if 'ŕ' in s:font='latin'
  # Mixed Korean runs use the actual Korean face.
  if any('\uac00'<=c<='\ud7af' for c in s) and font in ['reg','bold']:font='ko'
  if any(ord(c)>255 for c in s) and font in ['wide','cond']:font='bold'
  natural=self.width(s,size,font)
  if width and natural>width:size*=width/natural
  entry={'text':s,'x':x,'y':y,'size':size,'font':font,'module':self.module};self.log.append(entry)
  self.p.append(f'<g aria-label="{html.escape(s,quote=True)}" transform="translate({x},{y})'+(f' rotate({rotate})' if rotate else '')+f'" fill="{color}" opacity="{opacity}">')
  cur=0;boxes=[]
  for ch in s:
   f,cm,gs,up,actual_font=self.charfont(ch,font)
   g=cm[ord(ch)];gid=actual_font+'_'+str(ord(ch))
   bp=BoundsPen(gs);gs[g].draw(bp)
   if bp.bounds:
    x0,y0,x1,y1=bp.bounds;boxes.append((x+cur+x0*size/up,y-y1*size/up,x+cur+x1*size/up,y-y0*size/up))
   if gid not in self.defs:
    pen=SVGPathPen(gs);gs[g].draw(pen);self.defs[gid]=f'<path id="{gid}" d="{pen.getCommands()}"/>'
   self.p.append(f'<use href="#{gid}" transform="translate({cur},0) scale({size/up}, {-size/up})"/>');cur+=gs[g].width*size/up
  if boxes:entry['bbox']=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
  self.p.append('</g>');return cur
 def logos(self,x,y,w=1080):
  for i,(key,bw) in enumerate([('lalm',75),('cement',130),('museum',52),('council',120),('fund',130)]):
   im=Image.open(next(AS.glob(key+'.*'))).convert('RGB');r,g,b=im.split();mask=ImageChops.darker(ImageChops.darker(r,g),b).point(lambda z:255 if z<205 else 0);box=mask.getbbox();im=im.crop(box)
   import io
   out=io.BytesIO();im.save(out,format='PNG');data=base64.b64encode(out.getvalue()).decode()
   cell=w/5;self.rect(x+i*cell,y,cell-8,58,'#ffffff')
   self.p.append(f'<image x="{x+i*cell+5}" y="{y+4}" width="{cell-18}" height="50" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')
 def save(self,id):
  svg='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="1800" viewBox="0 0 1200 1800"><defs>'+''.join(self.defs.values())+'</defs>'+''.join(self.p)+'</svg>'
  (R/'sources'/f'{id}.svg').write_text(svg);(R/'design'/f'{id}.text.json').write_text(json.dumps(self.log,ensure_ascii=False))
def attrs(d):return ' '.join(f'{k.replace("_","-")}="{v}"' for k,v in d.items())
def details(a,x,y,w=430,scale=1):
 a.module='details'
 a.group(f'translate({x},{y}) scale({scale})');x=y=0
 lines=[('LALM 项目资料交流展',0,25,'bold'),('Project Materials Exhibition of Project',27,14,'reg'),('2026.11.19–11.21',70,32,'wide'),('10:00–18:00',103,23,'reg'),('丄美术馆 · 杭州',147,27,'bold'),('开幕现场导览',188,18,'bold'),('11.21｜14:00–15:30',214,19,'reg'),('我们不知道—开放现场',250,18,'bold'),('11.21｜16:00–18:00',276,19,'reg'),('工作团队 / WORK TEAM',316,15,'bold'),('问地 Wen-Di Wu · 王一土 Wang Yitu',341,15,'reg'),('吕德生 Lyu Desheng',364,15,'reg'),('观察员 / OBSERVERS',397,15,'bold'),('（    ）· 王一土 Wang Yitu · 郑一方 Zheng Yifang',422,15,'reg'),('主办 Organizer：水泥公园 CementPark',457,15,'reg'),('协办 Co-organizer：丄美术馆 Shang Art Museum',480,15,'reg'),('地址 Venue',513,14,'bold'),('浙江省杭州市萧山区河上镇',537,15,'reg'),('下门村泽坞墅2号，丄美术馆',560,15,'reg'),('Shang Art Museum, No. 2, Zewushu, Xiamen Village,',585,12,'reg'),('Heshang Town, Xiaoshan District, Hangzhou, Zhejiang Province',604,12,'reg')]
 if a.lang in LOCALES:
  localized=LOCALES[a.lang]['details']
  assert len(localized)==len(lines),(a.lang,len(localized))
  lines=[(item['text'],base[1],base[2],base[3]) for item,base in zip(localized,lines)]
 for s,dy,sz,f in lines:a.text(s,0,dy,sz,f,width=w)
 a.end()
 a.module=None
def roster(a,x,y,w=610,scale=1,columns=False):
 a.module='roster'
 a.group(f'translate({x},{y}) scale({scale})');cut=w*.64
 if a.lang in LOCALES:
  loc=LOCALES[a.lang];labels=loc['labels']
  a.text(labels['project'],0,0,20,'bold',width=cut-15);a.text(labels['attendees'],cut,0,20,'bold',width=w-cut)
  a.line(0,23,w,23,a.ink,.7)
  for i,r in enumerate(loc['roster']):
   yy=62+i*(39*13/14)
   a.text(r['project'],0,yy,19,'bold',width=cut-15);a.text(r['name'],cut,yy,18,'bold',width=w-cut)
   # Original identities are subordinate anchors, never untranslated instructions.
   if a.lang=='EN':
    a.text(r['project_zh'],0,yy+16,11,'reg',width=cut-15);a.text(r['name_zh'],cut,yy+16,11,'reg',width=w-cut)
   else:
    a.text(r['project_original'],0,yy+16,11,'latin',width=cut-15);a.text(r['name_original'],cut,yy+16,11,'latin',width=w-cut)
 else:
  a.text('空间／项目',0,0,20,'bold');a.text('参会者',cut,0,20,'bold')
  a.text('Space / Project',0,24,12,'latin');a.text('Attendees',cut,24,12,'latin')
  for i,r in enumerate(ROWS):
   yy=62+i*(39*13/14)
   a.text(r['zh'],0,yy,18,'bold',width=cut-15);a.text(r['en'][0],0,yy+16,12,width=cut-15)
   a.text(r['name'][0],cut,yy,17,'bold',width=w-cut);a.text(r['name'][1],cut,yy+16,12,width=w-cut)
 a.end()
 a.module=None
def info(a,mode,paper,ink):
 old=a.ink;a.ink=ink;a.in_info=True
 if mode=='bottom':
  a.rect(0,1130,1200,670,paper);details(a,48,1180,500,0.83);roster(a,500,1170,720,.90);a.logos(48,1710,1104)
 elif mode=='top':
  a.rect(0,0,1200,660,paper);details(a,48,65,430,.86);roster(a,485,58,720,.87);a.logos(48,590,1104)
 elif mode=='left':
  a.rect(0,0,435,1800,paper);details(a,38,70,420,.86);roster(a,38,690,430,.85);a.logos(38,1570,360)
  a.text('我们知道 / We Know',38,1715,19,'bold',width=360)
 elif mode=='right':
  a.rect(765,0,435,1800,paper);details(a,800,70,420,.86);roster(a,800,690,430,.85);a.logos(800,1570,360);a.text('我们知道 / We Know',800,1715,19,'bold',width=360)
 elif mode=='middle':
  a.rect(0,610,1200,665,paper);details(a,48,661,430,.86);roster(a,485,651,720,.87);a.logos(48,1200,1104)
 elif mode=='split':
  a.rect(0,0,470,700,paper);details(a,45,65,430,.90)
  a.rect(480,1040,720,760,paper);roster(a,515,1090,690,.93);a.logos(515,1700,640)
 elif mode=='receipt':
  details(a,55,70,620,.70);roster(a,55,650,760,1.43);a.logos(55,1700,1090)
  for i in range(16):a.line(55,715+i*(55.77*14/15),1145,715+i*(55.77*14/15),ink,.5)
 elif mode=='windows':
  a.rect(535,0,665,650,paper);roster(a,575,65,665,.88)
  a.rect(0,1120,530,680,paper);details(a,50,1180,500,.85);a.logos(570,1690,580)
 elif mode=='register':
  a.rect(48,390,1104,1230,paper);details(a,85,460,440,.96);roster(a,575,460,540,.96);a.logos(85,1450,1030)
 a.ink=old;a.in_info=False

def title(a,lang,x,y,width=1080,size=220,font='bold',color=None):
 text={'ZH':'我们知道','EN':'WE KNOW','JA':'私たちは知っている','KO':'우리는 알고 있다','IN':'हम जानते हैं'}[lang]
 f=TITLE_FONTS.get(a.id,{'JA':'jp','KO':'ko'}.get(lang,font));a.text(text,x,y,size,f,color,width)
 # Locked bilingual identity remains a modest anchor.
 if lang!='ZH':a.text('我们知道',x,y+42,22,'bold',color,width)
 if lang!='EN':a.text('We Know',x,y+72,20,'wide',color,width)

def dots(a,file,x,y,w,h,c):
 p=R/'design'/file
 if not p.exists():return
 im=Image.open(p).convert('L').resize((110,150))
 for yy in range(150):
  for xx in range(110):
   k=1-im.getpixel((xx,yy))/255
   if k>.04:a.circle(x+(xx+.5)*w/110,y+(yy+.5)*h/150,round((w/110)*.47*math.sqrt(k),2),c)

def art(id):
 spec=SPECS[id];bg,ink,accent=spec['colors'];a=Art(bg,ink,id);lang=id[:2];mode=spec['layout']
 if id=='ZH01':
  a.rect(0,0,1200,1100,ink);a.text('我们',-28,510,560,'songBold',bg,1250);a.text('知道',-28,1040,560,'songBold',bg,1250)
  a.path('M0,435 L1200,335 L1200,390 L0,490',bg);a.text('We Know',65,1095,36,'wide',bg)
 elif id=='ZH02':
  dots(a,'hands.png',70,40,1060,1100,ink);a.rect(0,810,680,190,bg);title(a,lang,65,925,610,117,color=accent)
 elif id=='ZH03':
  for i in range(4):a.text('我们知道',45,880+i*260,248,'qing',ink,1110)
  a.rect(0,1568,1200,65,bg);a.text('We Know',75,1770,80,'wide',ink)
 elif id=='ZH04':
  for i in range(7):a.path(f'M{470+i*36},150 L{1120-i*12},310 L{1050-i*20},1520 L{460+i*33},1400',accent,opacity=.16)
  for i,ch in enumerate('我们知道'):a.text(ch,570+i*37,450+i*300,235,'song',ink)
  a.text('We Know',490,1720,52,'wide')
 elif id=='ZH05':
  for yy in range(70,1790,96):a.line(45,yy,1155,yy,accent,1)
  title(a,lang,70,290,1060,210);a.text('2026',70,1750,130,'cond',accent)
 elif id=='ZH06':
  for i in range(11):
   a.group(f'translate(600,535) rotate({i*18-90})');a.text('我们知道',-460,-140-i*9,60+i*3,'bold',ink,900,opacity=.18+i*.07);a.end()
  title(a,lang,80,1005,1050,110)
 elif id=='ZH07':
  a.path('M0,0 L720,0 L540,1800 L0,1800',accent)
  for i,ch in enumerate('我们知道'):a.group(f'translate(70,{380+i*340}) rotate(-12)');a.text(ch,0,0,320,'wenkai',bg);a.end()
  a.text('We Know',80,1750,44,'wide',bg)
 elif id=='ZH08':
  for i,ch in enumerate('我们知道'):
   a.group(f'translate({60+(i%2)*320},{630+(i//2)*590}) rotate({[-8,5,3,-5][i]})');a.text(ch,0,0,340,'brush',ink);a.end()
  random.seed(8)
  for _ in range(95):
   x=random.randint(50,700);y=random.randint(250,1270);a.path(f'M{x},{y} l{random.randint(20,120)},-8',stroke=bg,sw=random.choice([1,2,3]))
  a.text('We Know',65,1550,74,'wide')
 elif id=='ZH09':
  dots(a,'paper.png',0,0,1200,1800,ink)
  for yy in range(90,1100,90):a.line(25,yy,110,yy,accent,3)
  a.rect(70,760,1060,250,bg);title(a,lang,110,910,1000,170,color=ink)
  a.circle(280,350,170,'none',stroke=accent,stroke_width=3);a.line(280,520,280,720,accent,3)
 elif id=='ZH10':
  a.rect(572,350,5,480,accent);a.text('我们知道',610,515,78,'wenkai',width=535);a.text('We Know',610,565,20,'serif')
  a.path('M577,830 l125,-55 l-125,15',accent)
 elif id=='EN01':
  for txt,x,y,sz in [('WE',40,340,220),('KNOW',60,910,190),('WE',320,1450,120)]:a.text(txt,x,y,sz,'wide',ink,690)
  for x,y,X,Y in [(80,430,650,790),(130,990,400,1280),(80,430,400,1280)]:a.line(x,y,X,Y,ink,3)
  for x,y in [(80,430),(650,790),(400,1280)]:a.circle(x,y,17,ink)
  a.text('我们知道',65,1680,32,'bold')
 elif id=='EN02':
  a.group('translate(505,105) scale(.65,1.95)');a.text('WE',0,380,400,'cond',ink,960);a.text('KNOW',0,760,400,'cond',ink,960);a.end();a.text('我们知道',500,1730,38,'bold')
 elif id=='EN03':
  dots(a,'hands.png',240,710,810,1000,ink);a.rect(0,1050,1200,215,accent);a.text('WE KNOW',40,1215,200,'cond',bg,1120);a.text('我们知道',60,1740,34,'bold')
 elif id=='EN04':
  a.path('M0,0 L1200,0 L1200,900 L800,1100 L200,950',accent)
  a.path('M800,0 L600,960 L800,1100 L1000,150',bg);a.path('M800,0 L750,1060 L800,1100 L1000,150',ink,opacity=.14)
  a.text('WE',60,330,330,'wide',bg);a.text('KNOW',60,690,290,'cond',bg,1100);a.text('我们知道',65,1030,36,'bold',ink)
 elif id=='EN05':
  for y in range(30,1770,40):a.circle(1190,y,5,accent)
  a.text('WE',600,260,225,'serif',accent,550);a.text('KNOW',580,470,180,'serif',accent,570)
  a.text('我们知道',620,540,30,'bold');a.rect(55,600,1090,8,accent)
 elif id=='EN06':
  a.path('M470,0 L1200,0 L1200,1040 L480,1040 L480,1800 L0,1800 L0,700 L470,700',accent)
  a.text('WE',550,400,320,'wide',bg,590);a.text('KNOW',55,1080,120,'wide',ink,420);a.text('我们知道',55,1140,32,'bold');a.line(540,475,1040,940,bg,10)
 elif id=='EN07':
  a.circle(600,480,330,ink);a.circle(600,480,205,bg);a.rect(530,60,140,880,bg);a.rect(530,390,140,180,ink)
  a.text('WE KNOW',70,1080,150,'wide',ink,1060);a.text('我们知道',75,1115,25,'bold')
 elif id=='EN08':
  for dx,c in [(7,accent),(-7,ink)]:
   a.text('WE',60+dx,1090,410,'wide',c);a.text('KNOW',60-dx,1570,320,'cond',c,1080)
  a.text('我们知道',70,1740,40,'bold',ink)
 elif id=='EN09':
  for x,y in [(450,60),(1150,60),(450,1740),(1150,1740)]:a.line(x,y,780,900,accent,3)
  a.path('M540,380 L1080,510 L1050,1420 L550,1510 Z',stroke=ink,sw=3)
  a.group('translate(570,440) skewY(13)');a.text('WE',0,230,220,'serif',ink,470);a.text('KNOW',0,650,200,'serif',ink,460);a.end();a.text('我们知道',490,1690,30,'bold')
 elif id=='EN10':
  a.text('WE KNOW',55,380,220,'cond',accent,1090);a.text('我们知道',60,460,30,'bold',accent)
  for i,y in enumerate(range(1330,1750,35)):
   a.line(50,y,1150,y,accent,2);a.rect(180+(i*83)%750,y-9,130,18,accent)
 elif id=='KO01':
  a.rect(0,0,1200,610,ink);a.text('우리는',50,252,260,'ko',bg,1090);a.text('알고 있다',50,535,260,'ko',bg,1090)
  a.text('우리는',60,1485,180,'ko',ink,1080);a.text('알고 있다',60,1710,220,'ko',ink,1080);a.text('我们知道 / We Know',70,1760,22,'bold')
 elif id=='KO02':
  a.path('M90,1700 C970,1550 -50,790 1050,870 C700,1250 650,1600 1140,1730',stroke=accent,sw=7)
  a.text('우리는',75,1080,240,'koSerif',ink,1030);a.text('알고 있다',75,1395,240,'koSerif',ink,1050);a.text('我们知道 / We Know',80,1730,24,'bold')
 elif id=='JA01':
  a.rect(760,700,160,800,accent);a.rect(460,840,160,865,accent)
  for i,ch in enumerate('私たちは'):a.text(ch,770,900+i*180,150,'jpv',ink)
  for i,ch in enumerate('知っている'):a.text(ch,470,1025+i*160,145,'jpv',ink)
  a.text('我们知道 / We Know',60,1740,28,'bold',ink,450)
 elif id=='JA02':
  for i in range(8):a.rect(75+i*28,90+i*80,940-i*55,860-i*36,accent,opacity=.10)
  for i in range(3):a.text('私たちは知っている',40+i*20,390+i*245,160,'jpSerif',ink if i==2 else accent,1100)
  a.text('我们知道 / We Know',65,1070,30,'bold')
 elif id=='IN01':
  for i in range(8):a.path(f'M30,{180+i*195} C630,{100+i*195} 100,{500+i*150} 720,{300+i*180}',stroke=accent,sw=5)
  for word,x,y,sz in [('हम',55,490,400),('जानते',55,1000,360),('हैं',330,1490,430)]:
   a.text(word,x,y,sz,'bold',ink,width=710-x)
  a.text('我们知道 / We Know',65,1710,25,'bold')
 elif id=='IN02':
  for i in range(7):a.rect(65+i*8,70+i*6,1070-i*16,950-i*12,accent,opacity=.08)
  for word,baseline,sz in [('हम जानते',490,270),('हैं',890,390)]:
   sz=min(sz,sz*1030/shaped_width(word,sz));xx=(1200-shaped_width(word,sz))/2
   for dx,dy,col in [(5,5,accent),(-4,-3,'#fffdf4'),(0,0,ink)]:a.text(word,xx+dx,baseline+dy,sz,'bold',col)
  a.text('我们知道 / We Know',90,1040,30,'bold')
 info(a,mode,spec['paper'],bg if id in ['ZH03','EN10'] else ink)
 # Title identity is already in composition; body always preserves all locked data.
 a.save(id);return a

# Each row supplies a different composition mechanism, not a color/locale replacement.
TABLE=[
('ZH01','缺失的共识','bottom','#ffffff','#111111','#777777','负形中的缺口成为共同认知的边界。','超大字双行／负形切口','黑体负形','标题空缺','高密度上部→信息底部'),
('ZH02','身体的证词','bottom','#e4e0db','#3e3836','#8b2327','手掌接触看不见的表面，知道来自身体的阻力。','摄影网点／左下标题','克制黑体','原创摄影转矢量网点','触感图像→精确信息'),
('ZH03','公共声明','top','#2249ce','#f8f6ed','#16298b','重复的确定声明被一条空白打断。','上置信息／整行文字场','整行黑体','重复与擦除','小字入口→向下重复'),
('ZH04','知识的剖面','left','#dedbe4','#302c3e','#9c90b2','只有透过多层边界才能辨认一句话。','左索引／纵向层叠','单字纵深','半透明矢量材料','左→层层向右'),
('ZH05','集体档案','register','#eee9db','#173d2b','#72836b','名单与刻度把分散的经验收进同一份档案。','登记索引／中部双栏','理性编号式字','横向索引线','标题→并列档案'),
('ZH06','知道的回声','bottom','#f48232','#33143f','#cc5328','同一句话沿不同角度传播而不重合。','放射文字路径','旋转黑体','回声文字','旋转阅读→底部停顿'),
('ZH07','不稳定的秩序','right','#f6cdd0','#9e2026','#d83a35','每个字都按同一斜率偏离稳定轴。','右侧静态／左侧倾斜','倾斜厚字','偏心色面','对角上升→右侧核对'),
('ZH08','手的记忆','right','#d9b65e','#282722','#a47d30','印刷字像被手工反复擦印，保留未能完全复制的痕迹。','右侧资料／四个独立拓印','磨损字形','原创矢量拓印','四字游走→边栏'),
('ZH09','局部成为整体','windows','#daeaf1','#382c28','#467689','纸纤维被放大成无法轻易定位的边界。','微观图像穿插对角资料窗口','测量式标题','原创微观影像转网点','微观→标题→信息'),
('ZH10','迟疑的确定','split','#f6f4ec','#172b4a','#172b4a','细线的突然折返让一句肯定停顿。','对角双区／大留白','小型清晰标题','一根折线','空白→细小主题→名单'),
('EN01','A shared field','right','#d9f05b','#141916','#5f7730','WE与KNOW在多个节点之间建立共同关系。','多中心关系／右侧清单','宽体散置','节点与连接','游走式阅读'),
('EN02','A statement under pressure','left','#f5f0e4','#171715','#c5bda6','窄长英文承担受压结构的重量。','左注释／纵向文字柱','极窄长体','字形纵向压力','上下牵引'),
('EN03','An image withheld','top','#dcd8d0','#682127','#982a34','被文字遮住的触碰，让观看只能获得局部证词。','顶部资料／下方遮挡摄影','窄体覆盖条','摄影网点与遮挡','信息→缺失图像'),
('EN04','Reading through a fold','bottom','#ddd1b7','#133d9d','#284bc6','折面让阅读跨越同一纸张的两个方向。','纸面折角／底部资料','大宽体与窄体','原创折纸矢量','折角引导阅读'),
('EN05','The register','receipt','#f2eade','#601f37','#7b263e','每个参与者成为连续登记中的一条证据。','上部双域／名单放大为连续登记','票据窄体','序列与穿孔','纵向连续登记'),
('EN06','Between two voices','split','#f28744','#163f51','#3d93a2','两种声音在错位而非均分的区域中相遇。','交错双区','宽体问答','不对称色域','对角回应'),
('EN07','One signal','bottom','#eff45b','#292a29','#888b30','断开的圆环让完整与缺失共存。','单一大符号／标题底座','极少量宽体','原创缺口环','中心凝视→信息'),
('EN08','Almost aligned','top','#f6f2e8','#253d98','#cc3b3b','同一句话的两个印版几乎重合，仍留下偏差。','信息在上／分色文字在下','受控套印','红蓝矢量错位','轮廓校准'),
('EN09','A room of words','left','#c9d2c8','#253b34','#edf0e9','字成为房间的一面墙，位置改变所知。','左资料／右透视房间','透视宽体','线性空间模型','入口→深处'),
('EN10','An interrupted broadcast','middle','#202e65','#f1e6a3','#e5ce70','可读信号之间的停顿比信号本身更长。','上下信号被中央信息打断','窄体信号','有序中断线','脉冲式阅读'),
('KO01','语块的构筑','middle','#efc577','#162c50','#29466e','完整韩文字块像可组合建筑，但不拆散音节。','上下标题／中间信息','韩文字块','模块文字','两端聚合'),
('KO02','轻声的共同体','top','#dce9d5','#303b35','#6b886f','手势路径将间隔很远的文字联系起来。','上资料／下方开放手势','韩文轻盈排字','连续手绘曲线','舒缓横向'),
('IN01','连续的认知','right','#cae0e6','#7f3229','#a94830','完整天城文字在连续笔势中保持读音。','右资料／左笔势','HarfBuzz天城文拟音','连续贝塞尔笔势','沿流线观看'),
('IN02','共同的印记','bottom','#eee8d9','#181817','#d99826','重复压印让共同经验留下不完全相同的边。','中央印痕／底部资料','HarfBuzz天城文拟音','多重压印矢量','层层显影'),
('JA01','可见与不可见','top','#f2e6ab','#161716','#e8d475','纵向音译标题在白空间里建立可见的读取路径。','上置信息／下方纵向音译','日文纵排','竖向空白','纵向穿行'),
('JA02','复写中的差异','bottom','#dedce4','#363443','#bf6d3b','复写的同一句话总会错开一个位置。','上部复写／下部资料','日文横向复写','透明片层','叠影→清晰锚点'),
]
SPECS={}
for id,title_,layout,bg,ink,accent,concept,skeleton,type_,medium,reading in TABLE:
 # Reverse dark-on-light information where the composition background is dark.
 paper=bg
 if id in ['ZH03','EN10']:paper=ink;ink_for_body=bg
 else:ink_for_body=ink
 SPECS[id]={'id':id,'title':id,'language':id[:2],'layout':layout,'colors':[bg,ink,accent],'paper':paper,'concept':concept,'skeleton':skeleton,'typography':type_,'medium':medium,'reading':reading}
for id in TITLE_FONTS:
 SPECS[id]['typography']={'title_font':TITLE_FONTS[id],'body_fonts':BODY_FONTS[id]}
for id in ['JA01','JA02','KO01','KO02','IN01','IN02']:
 SPECS[id]['typography']='Full-page localized typography'
 SPECS[id]['concept']='Natural-language theme, localized details and phonetic proper-name identities.'
# Ensure text on light information panels is dark for two dark-field cases.
if __name__=='__main__':
 (R/'design'/'matrix.json').write_text(json.dumps(list(SPECS.values()),ensure_ascii=False,indent=2))
 ids=sys.argv[1:] or list(SPECS)
 for id in ids:
  a=art(id);print(id,len(a.log),flush=True)
