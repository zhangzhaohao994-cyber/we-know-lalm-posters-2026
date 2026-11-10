# 新增字体：中文主视觉与正文的真正性格差异

2026-11-10 从 Google Fonts 官方 google/fonts 仓库及 LXGW 作者仓库下载。全部为 SIL OFL 1.1；完整许可证和原始来源 URL 已保留。仅新增字体及审计，不修改 design/render.py。

## 可直接加载的字体文件

| 文件 | 性格／真实字重 | 推荐用途 |
|---|---|---|
| LALM-NotoSerifSC-Regular.ttf | 中文宋体，真实400静态实例 | 清晰的宋体内文、小标题、留白方向 |
| LALM-NotoSerifSC-Bold.ttf | 中文宋体，真实700静态实例 | 锐利衬线主视觉、正文层级 |
| LALM-WenKai-Regular.ttf | 霞鹜文楷，真实400 | 有书写气息的标题和完整内文 |
| LALM-MaShanZheng-Regular.ttf | 马善政毛笔楷书，真实400但视觉较重 | 标题；不可冒称本项目原创手写 |
| LALM-XiaoWei-Regular.ttf | 站酷小薇，楔形/宋体风格，真实400 | 主标题和短栏目，不建议直接覆盖全部内文 |
| LALM-QingKeHuangYou-Regular.ttf | 站酷庆科黄油，圆角窄体，真实400 | 声明、重复文字、模块标题 |
| LALM-NotoSerifJP-Regular.ttf / -Bold.ttf | 日文区域明朝体，真实400/700 | 日文标题及全文；简体中文锚点仍需SC回退 |
| LALM-NotoSerifKR-Regular.ttf / -Bold.ttf | 韩文明朝体，真实400/700 | 韩文标题及全文；中文锚点仍需SC回退 |

上述10个TTF共2,695,908字节（约2.57MiB），最大单文件372,352字节，远低于GitHub单文件限额。全部是项目字符子集，不是完整字体库。原始大字体总计约109MB只保留于 research/private/font-originals，禁止误打包进公开源ZIP。

## 字形覆盖

依据：锁定 final-layout.json 所有正文、15组名单、实际26款text.json中的文字、新版 content/localizations.json 全文、全部ASCII和常用标点。原锁定所需中文148种，扩充日文汉字与完整各语正文后171种。所有源语言文本递归纳入字符集，不只纳入原标题。

- 五种中文字体都完整支持“我们知道”。
- Noto Serif SC、文楷覆盖全部171种必需中文及汉字，包括“丄”和“水田部落行為藝術營、貓蚯蚓”。
- 文楷还覆盖本项目所需日/韩全文字形和重音字母“ŕ”；不支持本项目天城文字，应交给既有Devanagari shaping管线。
- 在原锁定中文中，马善政与小薇缺“丄為營藝術貓”；庆科缺“為貓”。新加入日文汉字后缺字列表更长，详见new-font-audit.json。它们的常用标题不受影响，但不能不加回退就用于完整名单。
- Noto Serif SC 不含 ŕ 与所需韩文；英文 Studio eŕté 可继续用既有 NotoSans-Regular.ttf，韩文用KR或文楷；应按语言段/字符回退，不擅自删除字符。
- JP/KR区域字体支持对应标题和新版本全文。韩文目标全文缺字为0；日文目标全文仅地址中的简体“坞泽镇”在JP原字体中缺失，应回退同字重SC宋体。独立验证见 localized-font-coverage.json。含简体中文身份锚点时还有其他简体字，应继续回退SC或文楷，不删除字符。
- 所有原始字形保持；变量字体通过fontTools静态实例化真实400/700字重，没有模拟描边加粗。
- JP子集保留全部OpenType layout features，包括竖排替代特性。继续复用渲染器的GSUB vert逻辑，不能把长音符硬画成横杠。

## 字体命名与许可证

子集与静态实例属于修改版本，内部family/full/PostScript名称已加LALM项目名称，并将文楷family改为“LALM WenKai”，避开原作者保留字“LXGW/霞鹜”。name表的Regular/Bold子族与真实字重一致。原作者copyright和OFL条款保留；原始来源记录在NEW-FONT-SOURCES.json。

子集不代表获取了额外的Logo或参考图权利。作者字体不是本项目原创字体。字体可按所附OFL与作品源文件一起分发，不应单独出售字体。

## 按海报搭配

详见 typography-recommendations.json。建议主视觉至少有宋、楷、毛笔、楔形宋、圆角窄体五种角色；正文至少在无衬线、宋体、文楷三种之间有真实变化。不能把“更换一个字体文件”当作全部设计返工，需要同时调整标题比例、行距、留白、信息的编辑方式。

new-font-proof.jpg 已实际打开视觉检查，展示各中文字体真实轮廓和内文性格。不能继续声称“刮擦后的黑体”为手写。马善政是有实际笔势的已授权字体，若使用应这样准确描述。
