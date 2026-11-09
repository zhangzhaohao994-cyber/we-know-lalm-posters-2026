# We Know · LALM 2026

27 张海报画廊：1 张用户已确认的原版，26 个新设计方向。

展示次序：ORIGINAL → JA01–02 → KO01–02 → IN01–02 → ZH01–10 → EN01–10。

## 内容与语言

锁定活动为 **LALM 项目资料交流展**，2026.11.19–11.21，丄美术馆。14组机构与艺术家按既有英文A–Z顺序呈现，完整对应见 `content/`。此网站是视觉提案画廊，非机构官方网站。

日韩和印地语主标题按指定规则对既有英文标题 We Know 作拟音，原中文及英文身份仍保留。印地语为用户明确选择的设计语言，不据此断言参与者母语。新增语言写法经过字体/塑形检查，未声称经过母语者审校。

## 文件

- `previews/`：1200×1800网页预览；ORIGINAL保留原GIF。
- `print/`：26个7087×10630 PNG，300 PPI、sRGB。ORIGINAL是保留的1200×1800旧稿，不冒充印刷高清。
- `sources/`：真实SVG矢量图形及字体轮廓，文字具有aria-label与结构记录。
- `design/render.py`：可编辑排版逻辑；`design/*.text.json`是准确文本及字体记录。
- `assets/`：用户提供的品牌标志；`fonts/`：附许可的开放字体。
- `research/references.json`：26个实际查看的参考锚点，仅公开来源链接及观察，不发布参考图片。
- `qa/`：内容、视觉审查与修订记录；`QUALITY.md`说明核验范围。

## 复现

Python 3.11+：`pip install pillow fonttools uharfbuzz`

Node 20+：`npm install sharp@0.35.5`

运行 `python design/render.py` 生成SVG；运行 `node design/export.cjs` 生成网页预览；运行 `node design/export.cjs --print` 从SVG直接生成全尺寸PNG。英文和中日韩正文转为真实字体轮廓，印地语由HarfBuzz塑形后转轮廓；无需浏览器动态替换字体。

SVG的viewBox是1200×1800；高清导出将SVG输出尺寸设为7087×10630后直接光栅化，未把小尺寸预览放大。嵌入的logo保持原图，尺寸克制；摄影意象先转换为显式矢量网点，网点是最终造型，不宣称为高分辨率摄影细节。

`design/hands.png` 与 `design/paper.png` 是为本项目使用内置图像生成工具制作的原创视觉素材，不是活动现场纪实照片。用于ZH02/EN03/ZH09的网点图形。随机拓印擦痕种子固定为8。

## 发布

静态HTML/CSS/JS，GitHub Pages。仅公开本项目文件。原始委托提示词、参考原图、本机路径、认证资料及其他项目均不在发布内容中。
