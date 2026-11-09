"""HarfBuzz-shaped Devanagari SVG outlines, independent of render.py.

Install dependencies: pip install fonttools uharfbuzz==0.57.0
An optional LALM_LANGUAGE_DEPS environment variable can point to local dependencies.
Example: a.p.append(shaped_paths('वी नो', 240, x=50, y=330))
All positions use the SVG baseline convention (positive y downward).
The complete string is shaped as a run; do not split it into code points.
No letter spacing or artificial matra movement is applied.
"""
from functools import lru_cache
from pathlib import Path
from html import escape
import os
import sys

try:
    import uharfbuzz as hb
except ImportError:
    local_deps = Path(os.environ.get('LALM_LANGUAGE_DEPS', ''))
    if local_deps.is_dir():
        sys.path.insert(0, str(local_deps))
    import uharfbuzz as hb

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT_DIR = Path(__file__).resolve().parent.parent / 'fonts'


@lru_cache(maxsize=8)
def _load(path):
    data = Path(path).read_bytes()
    tt = TTFont(path)
    face = hb.Face(data)
    font = hb.Font(face)
    font.scale = (face.upem, face.upem)
    hb.ot_font_set_funcs(font)
    return tt, font, face.upem


def shape_run(text, size, *, font='Bold', font_path=None, x=0, y=0, fill='#000000'):
    """Return svg, advance_width, bbox and glyph audit for one shaped run.

    bbox is absolute (left, top, right, bottom), or None for whitespace.
    width is the pen advance, not necessarily the ink extent.
    """
    if size <= 0:
        raise ValueError('size must be positive')
    path = Path(font_path) if font_path else FONT_DIR / f'NotoSansDevanagari-{font}.ttf'
    tt, hbfont, upem = _load(str(path.resolve()))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = 'ltr'
    buf.script = 'Deva'
    buf.language = 'hi'
    hb.shape(hbfont, buf)
    order = tt.getGlyphOrder()
    glyphset = tt.getGlyphSet()
    scale = float(size) / upem
    cursor_x = cursor_y = 0
    paths = []
    bounds = []
    audit = []
    for gi, pos in zip(buf.glyph_infos, buf.glyph_positions):
        if gi.codepoint == 0:
            raise ValueError(f'Missing shaped glyph in {text!r} at cluster {gi.cluster}')
        name = order[gi.codepoint]
        gx = float(x) + (cursor_x + pos.x_offset) * scale
        gy = float(y) - (cursor_y + pos.y_offset) * scale
        transform = (scale, 0, 0, -scale, gx, gy)
        pen = SVGPathPen(glyphset)
        glyphset[name].draw(TransformPen(pen, transform))
        d = pen.getCommands()
        if d:
            paths.append(f'<path d="{d}"/>')
            bp = BoundsPen(glyphset)
            glyphset[name].draw(TransformPen(bp, transform))
            if bp.bounds:
                bounds.append(bp.bounds)
        audit.append({'gid': gi.codepoint, 'name': name, 'cluster': gi.cluster,
                      'x': gx, 'y': gy, 'x_advance': pos.x_advance * scale,
                      'x_offset': pos.x_offset * scale, 'y_offset': pos.y_offset * scale})
        cursor_x += pos.x_advance
        cursor_y += pos.y_advance
    bbox = (min(b[0] for b in bounds), min(b[1] for b in bounds),
            max(b[2] for b in bounds), max(b[3] for b in bounds)) if bounds else None
    svg = (f'<g aria-label="{escape(text, quote=True)}" fill="{escape(fill, quote=True)}">'
           + ''.join(paths) + '</g>')
    return {'svg': svg, 'advance_width': cursor_x * scale,
            'bbox': bbox, 'glyphs': audit, 'text': text,
            'font_file': path.name, 'shaper': 'HarfBuzz', 'hb_version': hb.version_string()}


def shaped_paths(text, size, *, font='Bold', font_path=None, x=0, y=0, fill='#000000'):
    """Return SVG <g> containing shaped path elements, ready to append."""
    return shape_run(text, size, font=font, font_path=font_path,
                     x=x, y=y, fill=fill)['svg']


def shaped_width(text, size, *, font='Bold', font_path=None):
    """Return shaped advance width for fitting and centering a complete run."""
    return shape_run(text, size, font=font, font_path=font_path)['advance_width']
