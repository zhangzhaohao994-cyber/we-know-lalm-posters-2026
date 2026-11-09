# 内容与语言审计

## 硬性文字来源
内容直接读取定稿 JSON。14组名单和全部94条真实渲染文字被保留；主标题“我们知道”为原图文字，已另列于 locked.title。

## 新语言标题规则
用户新提示词规定名字类专名新增跨语言形式按发音音译。采用已锁定的英文主题 We Know 作原始身份锚，可以提出日文「ウィー・ノウ」与韩文「위 노우」。这是从原英文发音直接转写，不是从中文临时音译再转写。它们是机器拟音方案，未获母语者审校，不标为官方译名。日/韩海报须标为语言待确认设计稿，锁定的 We Know / 我们知道 保留为辅助身份信息。

不将「私たちは知っている」「우리는 안다」作为正式新活动名直接使用；这些是含义翻译，和本次专名音译指示不同。普通栏目／角色词可作语义翻译，表格与专名对应表分开。

## 印度语言：已由用户指定印地语／天城文字
2026-11-10，用户明确回复「是，使用印地语（天城文字）」。因此 IN01/IN02 采用 Hindi / Devanagari（hi-Deva）。这是用户对本次视觉版本的语言选择，不是对参会者 Satadru Sovan 母语、偏好或本人的官方活动译名作出声明。

主标题拟音写作「वी नो」，原始身份锚为锁定英文 We Know /wiː noʊ/；同时保留 We Know / 我们知道。此写法采用长 ī 的「वी」和常见 know 发音转写「नो」。不用「वी नоу」，因为单独增加 उ 会造成多余的元音段；也不用「हम जानते हैं」作为新的专名，它属于含义翻译。此音译经过机器和字形审计，未经过印地语母语者审校，仍标为语言设计稿。

发音参考：
- Cambridge 的 know 发音：https://dictionary.cambridge.org/pronunciation/english/know （UK /nəʊ/，US /noʊ/）
- Shabdkosh 的 know 条目直接给出 IPA noʊ 和 Hindi 发音写法 नो：https://shabdkosh.com/dictionary/english-hindi/know/know-meaning-in-hindi

字体：官方 Google Fonts Noto Sans Devanagari，OFL 1.1。采用 HarfBuzz 对完整词组塑形，再用 fontTools 转轮廓，保证元音符号和字干位置关系。可重用接口见 design/devanagari_shape.py；实际粗体／常规体字形证明见 qa/devanagari-proof.png；无缺字。

此前提供的资料未指定 Satadru Sovan 希望使用哪种印度语言。本人英文网站公开履历与英文访谈仅能证实英文公开表达；出生于西孟加拉邦或现居新德里不等于应采用孟加拉语或印地语。

已查阅：
- 本人网站：https://satadrusovan.wordpress.com/home/
- 本人公开访谈：https://www.artamour.in/post/satadru-sovan-banduri-a-body-of-experiencing-phenomenal-art
- 画廊艺术家资料：https://galleryragini.com/satadru-sovan/

没有发现艺术家本人指定该项目印度文字的明确声明。未向艺术家发送消息；不以印度国籍推定母语。现有印地语选择完全以用户随后确认的设计要求为依据。

## 名字的边界
名单无需新增日语、韩语或印度语姓名。既有中英文形式作为锁定身份锚完整保留，避免对不明原读音多次转写。全部实体有稳定 ID，同名在团队与名单中的吕德生以及团队/观察员中王一土复用同一实体 ID。观察员空位保留。

## 规格
竖版；新稿7087×10630 px，300 PPI，PNG sRGB。原定稿仅有1200×1800静态稿与800×1200 GIF，不能插值后称为原生印刷高清。
