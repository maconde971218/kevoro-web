#!/usr/bin/env python3
"""Convierte nuestros SVG con texto a contornos autónomos de Manrope.
Uso: python marca/exportar-svg.py --font /ruta/a/Manrope.ttf
Dependencias de desarrollo: fonttools, brotli. No participa en el sitio web.
Fuentes de edición: marca/fuentes/{logos,posts}. Exporta marca/{logos,posts}.
"""
from pathlib import Path
import argparse
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
FONT = BASE.parent / 'assets/fonts/manrope-latin.woff2'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
FONTS = {}

def at(weight):
    if weight not in FONTS:
        font = TTFont(FONT)
        if 'fvar' in font:
            font = instantiateVariableFont(font, {'wght': weight}, inplace=True)
        FONTS[weight] = font
    return FONTS[weight]

def line_path(text, x, y, size, weight, spacing):
    font = at(weight)
    scale = size / font['head'].unitsPerEm
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    pen = SVGPathPen(glyphs)
    for letter in text:
        name = cmap.get(ord(letter))
        if name is None:
            raise ValueError(f'La fuente no contiene {letter!r}')
        glyph = glyphs[name]
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
        x += glyph.width * scale + spacing
    return pen.getCommands()

def replace_text(parent):
    for i, element in enumerate(list(parent)):
        if element.tag != f'{{{NS}}}text':
            replace_text(element)
            continue
        attrs = element.attrib
        x, y = float(attrs.get('x', 0)), float(attrs.get('y', 0))
        size = float(attrs.get('font-size', 16))
        weight = float(attrs.get('font-weight', 400))
        spacing = float(attrs.get('letter-spacing', 0))
        group = ET.Element(f'{{{NS}}}g', {'fill': attrs.get('fill', 'currentColor')})
        if 'transform' in attrs:
            group.set('transform', attrs['transform'])
        lines = list(element)
        if not lines:
            lines = [element]
        for line in lines:
            x = float(line.get('x', x))
            if line is not element:
                y = float(line.get('y', y)) + float(line.get('dy', 0))
            copy = line.text or ''
            path = line_path(copy, x, y, size, weight, spacing)
            ET.SubElement(group, f'{{{NS}}}path', {'d': path})
        parent.remove(element)
        parent.insert(i, group)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, default=FONT, help='Manrope TTF o WOFF2; WOFF2 requiere brotli')
    FONT = parser.parse_args().font
    for kind in ('logos', 'posts'):
        for source in sorted((BASE / 'fuentes' / kind).glob('*.svg')):
            tree = ET.parse(source)
            replace_text(tree.getroot())
            target = BASE / kind / source.name
            tree.write(target, encoding='unicode', xml_declaration=False)
            print(target.relative_to(BASE))
