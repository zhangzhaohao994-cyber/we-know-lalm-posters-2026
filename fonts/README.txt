Open fonts downloaded from official GitHub sources, 2026-11-10.

NotoSansCJKsc-Regular.otf / NotoSansCJKsc-Bold.otf
https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/SimplifiedChinese
NotoSansCJKjp-Bold.otf
https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/Japanese
NotoSansCJKkr-Bold.otf
https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/Korean
License: Noto-CJK-LICENSE.txt (SIL OFL 1.1).

Anton-Regular.ttf — https://github.com/google/fonts/tree/main/ofl/anton
ArchivoBlack-Regular.ttf — https://github.com/google/fonts/tree/main/ofl/archivoblack
NotoSans-Variable.ttf — https://github.com/google/fonts/tree/main/ofl/notosans
BodoniModa-Variable.ttf — https://github.com/google/fonts/tree/main/ofl/bodonimoda
Individual OFL files included.

NotoSans-Regular.ttf is a static instance generated from the variable font with wght=400, wdth=100.
BodoniModa-Regular.ttf and BodoniModa-Bold.ttf are static instances generated with opsz=72, wght=400/700.
Do not pretend these are distinct downloaded original static releases. Original variable source remains included.

FontTools cmap audit: CJK SC has no U+0155 (ŕ), so use NotoSans-Regular.ttf for Studio eŕté or per-character fallback. Other current locked text, including 丄 and the Korean string, is covered by CJK SC. JP and KR title forms are covered by the corresponding regional fonts. Do not substitute CJK SC forms for Japanese title kanji where regional variation matters.

Anton and Archivo Black have actual weight 400 although their visual shapes are heavy. Noto CJK Bold has weight 700. Do not apply simulated bold without documenting it.

System fonts (PingFang, Arial Black, Impact, Times, Apple SD Gothic Neo, Hiragino, Kohinoor) may be locally available, but they are not redistributed here and their availability is not proof of permission to bundle font binaries. Prefer the included OFL fonts for reproducible public sources.

License scope: OFL fonts can be used in artwork and bundled with required license notices; do not sell font software alone. This note is a usage summary, not a replacement for the included licenses.

NotoSansDevanagari-Variable.ttf — https://github.com/google/fonts/tree/main/ofl/notosansdevanagari
NotoSansDevanagari-Regular.ttf and -Bold.ttf are static instances generated with wght=400/700, wdth=100. License NotoSansDevanagari-OFL.txt.
Hindi title वी नो is shaped as a whole run with uharfbuzz 0.57.0 / HarfBuzz 15.0.0, then outlined via fontTools; see design/devanagari_shape.py and qa/devanagari-shaping.json.
