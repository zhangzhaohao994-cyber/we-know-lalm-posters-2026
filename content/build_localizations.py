"""Generate project-local translations without changing the approved source data."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
LOCKED = json.loads((ROOT / 'content.json').read_text())['locked']
BASELINES = [0,27,70,103,147,188,214,250,276,316,341,364,397,422,457,480,513,537,560,585,604]
IDS = ['exhibition','identity','dates','hours','venue_short','opening_tour','opening_time',
       'open_session','open_session_time','work_team_label','work_team_1','work_team_2',
       'observers_label','observers','organizer','coorganizer','address_label',
       'address_1','address_2','address_3','address_4']

PROJECTS = {
 'EN': [r['project']['en'].replace(' 페미날레','') for r in LOCKED['roster']],
 'JA': ['アルカリ','ビー・ビヨンド','セメントパーク','セメントパーク・東京',
        'フェイチュアン','フェミナーレ','ヘクシーダクシーボックス','クア・ジア',
        'オープンスペース','シャロウ・ブリージング','スタジオ・エルテ','ター・アカデミー',
        'ウォーターフィールド・スタジオ／キャットマオワーム','ズー'],
 'KO': ['알칼리','비비욘드','시멘트파크','시멘트파크 도쿄','페이촨','페미날레',
        '헥시덕시박스','콰자','오픈스페이스','샬로 브리딩','스튜디오 에르테',
        '타아카데미','워터필드 스튜디오／캣마오웜','주'],
 'IN': ['अल्कली','बीबियॉन्ड','सीमेंट पार्क','सीमेंट पार्क टोक्यो','फ़ेइचुआन','फ़ेमिनाले',
        'हेक्सी डक्सी बॉक्स','कुआ ज्या','ओपन स्पेस','शैलो ब्रीदिंग','स्टूडियो एर्ते',
        'ता अकैडमी','वॉटरफ़ील्ड स्टूडियो / कैटमाओवर्म','ज़ू'],
}
NAMES = {
 'EN': [r['person']['en'] for r in LOCKED['roster']],
 'JA': ['ハイエスト','ブライアン・パターソン','リュー・ドーション','大原由',
        'パン・チェンノン','ヨンジョン','サタドル・ソヴァン','ガオ・シュー',
        'チェン・ジン','ホアン・ゾンジェン','ロコ・ユハース','タイコノット',
        'チャン・ユエンシャン','ジン・ジンジン'],
 'KO': ['하이에스트','브라이언 패터슨','뤼더성','오하라 유','판천눙','연정',
        '사타드루 소반','가오쉬','천진','황쭝전','로코 유하스','타이코노트',
        '장위안샹','진진진'],
 'IN': ['हाइएस्ट','ब्रायन पैटरसन','ल्यु देशेंग','यू ओहारा','पान चेननोंग','यॉनजॉन्ग',
        'सताद्रु सोवन','गाओ श्यू','चेन जिन','हुआंग ज़ोंगझेन','रोको यूहास',
        'ताइकोनॉट','च्यांग युआन श्यांग','जिन जिनजिन'],
}
PEOPLE = {
 'EN': ['Wen-Di Wu','Wang Yitu','Lyu Desheng','Zheng Yifang'],
 'JA': ['ウェンディ・ウー','ワン・イートゥ','リュー・ドーション','ジョン・イーファン'],
 'KO': ['원디 우','왕이투','뤼더성','정이팡'],
 'IN': ['वेन-दी वू','वांग यीतू','ल्यु देशेंग','झेंग यीफांग'],
}
LANGS = {
 'EN': {
  'bcp47':'en','display_name':'English','title':'We Know',
  'labels':{'project':'Space / Project','attendees':'Attendees','work_team':'Work team',
            'observers':'Observers','organizer':'Organizer','coorganizer':'Co-organizer',
            'address':'Address','dates':'Dates','hours':'Opening hours'},
  'event':'LALM Project Materials Exhibition of Project',
  'venue':'Shang Art Museum · Hangzhou','museum':'Shang Art Museum',
  'opening':'Opening guided tour','open_session':"We Don’t Know — Open Session",
  'dates':'2026.11.19–11.21','tour_time':'11.21 | 14:00–15:30',
  'session_time':'11.21 | 16:00–18:00',
  'address':['Shang Art Museum, No. 2, Zewushu,','Xiamen Village, Heshang Town,',
             'Xiaoshan District, Hangzhou,','Zhejiang Province'],
 },
 'JA': {
  'bcp47':'ja','display_name':'日本語','title':'私たちは知っている',
  'labels':{'project':'スペース／プロジェクト','attendees':'参加者','work_team':'運営チーム',
            'observers':'オブザーバー','organizer':'主催','coorganizer':'共催',
            'address':'会場所在地','dates':'会期','hours':'開場時間'},
  'event':'LALM プロジェクト資料交流展',
  'venue':'シャン・アート・ミュージアム · 杭州','museum':'シャン・アート・ミュージアム',
  'opening':'開幕ガイドツアー','open_session':'私たちは知らない — オープンセッション',
  'dates':'2026年11月19日–21日','tour_time':'11月21日 | 14:00–15:30',
  'session_time':'11月21日 | 16:00–18:00',
  'address':['浙江省杭州市蕭山区','河上镇下门村',
             '泽坞墅2号','シャン・アート・ミュージアム'],
 },
 'KO': {
  'bcp47':'ko','display_name':'한국어','title':'우리는 알고 있다',
  'labels':{'project':'공간／프로젝트','attendees':'참가자','work_team':'운영팀',
            'observers':'옵서버','organizer':'주최','coorganizer':'공동주최',
            'address':'주소','dates':'기간','hours':'관람 시간'},
  'event':'LALM 프로젝트 자료 교류전',
  'venue':'샹 아트 뮤지엄 · 항저우','museum':'샹 아트 뮤지엄',
  'opening':'개막 현장 투어','open_session':'우리는 모른다 — 열린 현장',
  'dates':'2026.11.19–11.21','tour_time':'11월 21일 | 14:00–15:30',
  'session_time':'11월 21일 | 16:00–18:00',
  'address':['저장성 항저우시 샤오산구','허상진 샤먼촌','쩌우수 2호','샹 아트 뮤지엄'],
 },
 'IN': {
  'bcp47':'hi-Deva','display_name':'हिन्दी','title':'हम जानते हैं',
  'labels':{'project':'स्थान / परियोजना','attendees':'प्रतिभागी','work_team':'आयोजन दल',
            'observers':'पर्यवेक्षक','organizer':'आयोजक','coorganizer':'सह-आयोजक',
            'address':'पता','dates':'तिथियाँ','hours':'खुलने का समय'},
  'event':'LALM परियोजना सामग्री आदान-प्रदान प्रदर्शनी',
  'venue':'शांग आर्ट म्यूज़ियम · हांगझोउ','museum':'शांग आर्ट म्यूज़ियम',
  'opening':'उद्घाटन निर्देशित भ्रमण','open_session':'हम नहीं जानते — खुला सत्र',
  'dates':'19–21 नवंबर 2026','tour_time':'21 नवंबर | 14:00–15:30',
  'session_time':'21 नवंबर | 16:00–18:00',
  'address':['झेजियांग प्रांत, हांगझोउ, श्याओशान जिला',
             'हेशांग कस्बा, श्यामेन गाँव',
             'ज़ेवूशू, संख्या 2','शांग आर्ट म्यूज़ियम'],
 },
}

result = {
 'schema_version':1,
 'scope':'All 27 posters; user-added GRAVITATIONAL BODY and Lin Zhongfei included in 15 pairs',
 'instruction_precedence':'Latest user instruction requests full target-language presentation and natural semantic theme translation; supersedes earlier phonetic-only new theme policy.',
 'source_identity':'content.json locked and final-layout.json',
 'sort_rule':'Keep confirmed project Latin A–Z order; never resort by translated script or nationality.',
 'native_reviewed':False,
 'name_policy':'Use user-provided original forms when known; otherwise direct machine transliteration from confirmed Latin identity. Retain Latin and Chinese in data; never claim provisional forms are official names.',
 'layout_contract':{
  'details':'21 objects with original dy baselines; text may be empty. identity is an optional small source-title anchor.',
  'roster':'project/name are target-language primary; project_original/name_original are optional smaller Latin identity lines; Chinese fields are archival or optional tiny anchors, not mandatory three-language rows.',
  'fonts':'JA use Noto CJK JP, KO Noto CJK KR; Hindi must shape whole strings with HarfBuzz. Latin name eŕté needs Noto Sans coverage. Do not scale Hindi by code-point count.',
 },
 'languages':{},
}

for lang,project,name in [('JA','グラビテーショナル・ボディ','リン・ジョンフェイ'),('KO','그래비테이셔널 바디','린중페이'),('IN','ग्रैविटेशनल बॉडी','लिन झोंगफ़ेइ')]:
    PROJECTS[lang].insert(6,project);NAMES[lang].insert(6,name)

for code,cfg in LANGS.items():
    assert len(PROJECTS[code]) == len(NAMES[code]) == 15
    people = PEOPLE[code]
    sep = ' · '
    lbl = cfg['labels']
    detail_texts = [cfg['event'],'我们知道 / We Know',cfg['dates'],LOCKED['hours'],cfg['venue'],
       cfg['opening'],cfg['tour_time'],cfg['open_session'],cfg['session_time'],lbl['work_team'],
       sep.join(people[:2]),people[2],lbl['observers'],'(    )' + sep + sep.join([people[1],people[3]]),
       lbl['organizer'] + ': ' + PROJECTS[code][2],lbl['coorganizer'] + ': ' + cfg['museum'],
       lbl['address'],*cfg['address']]
    assert len(detail_texts)==21
    d={
      'bcp47':cfg['bcp47'],'display_name':cfg['display_name'],
      'title':cfg['title'],'title_mode':'semantic translation of 我们知道',
      'labels':lbl,'identity_anchor':{'title_zh':'我们知道','title_en':'We Know','venue_zh':'丄美术馆','venue_en':'Shang Art Museum'},
      'exhibition_original_en':LOCKED['event_name']['en'],
      'details':[{'id':id,'text':text,'dy':dy,'role':'small_identity_anchor' if id=='identity' else 'target_primary'} for id,text,dy in zip(IDS,detail_texts,BASELINES)],
      'roster':[],
      'work_team':[{'id':i['id'],'name':name,'original':i['en'],'zh':i['zh']} for i,name in zip(LOCKED['work_team'],people[:3])],
      'observers':[{'id':'observer_pending','name':'(    )','zh':'（    ）','status':'intentional_blank'},
                   {'id':'person_wangyitu','name':people[1],'original':'Wang Yitu','zh':'王一土'},
                   {'id':'person_zhengyifang','name':people[3],'original':'Zheng Yifang','zh':'郑一方'}],
      'review_status':'machine localization; native-language and proper-name approval pending' if code!='EN' else 'confirmed Latin identities retained; new ordinary-English labels machine translated, editorial review pending',
      'native_reviewed':False,
    }
    for idx,src in enumerate(LOCKED['roster']):
        row={'id':src['id'],'project_id':src['project_id'],'person_id':src['person_id'],
             'order':src['order'],'sort_key':src['sort_key'],
             'project':PROJECTS[code][idx],'name':NAMES[code][idx],
             'project_original':src['project']['en'],'name_original':src['person']['en'],
             'project_zh':src['project']['zh'],'name_zh':src['person']['zh'],
             'name_status':'confirmed supplied Latin' if code=='EN' else 'machine phonetic proposal from Latin; native review pending'}
        if code=='JA' and idx==3:row['name_status']='user-supplied Japanese original 大原由'
        if code=='KO' and idx==5:
            row['name_status']='연정 and 페미날레 attested in artist publication; Chinese 緣定 identifies same artist'
            row['evidence_url']='https://fliphtml5.com/riivd/ikzr/Yeonjeong_performance_2018-2019/5/'
        d['roster'].append(row)
    result['languages'][code]=d

(ROOT/'localizations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Saved localizations.json: 4 languages x 21 detail lines x 15 roster pairs')
