import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen

class RomanPolygonPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt): self.pen.moveTo(pt)
    def _lineTo(self, pt): self.pen.lineTo(pt)
    def _curveToOne(self, pt1, pt2, pt3): self.pen.lineTo(pt3)
    def _qCurveToOne(self, pt1, pt2): self.pen.lineTo(pt2)
    def _closePath(self): self.pen.closePath()
    def getGlyph(self): return self.pen.glyph()

def romanize(input_path, output_path):
    font = TTFont(input_path)
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT"]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"
    if "CFF " in font: del font["CFF "]

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    for glyph_name in font.getGlyphOrder():
        try:
            pen = RomanPolygonPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except:
            new_glyphs[glyph_name] = TTGlyphPen(glyphSet).glyph()

    font["glyf"].glyphs = new_glyphs
    font["maxp"].recalc(font)
    for glyph_name in font.getGlyphOrder():
        font["glyf"][glyph_name].recalcBounds(font["glyf"])
    font.save(output_path)

if __name__ == "__main__":
    romanize("SourceHanSans.ttf", "Max_Roman_Stone.ttf")
