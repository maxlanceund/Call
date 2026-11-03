import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen

class RomanPolygonPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        self.pen.moveTo(pt)

    def _lineTo(self, pt):
        self.pen.lineTo(pt)

    def _curveToOne(self, pt1, pt2, pt3):
        self.pen.lineTo(pt3)

    def _qCurveToOne(self, pt1, pt2):
        self.pen.lineTo(pt2)

    def _closePath(self):
        self.pen.closePath()

    def getGlyph(self):
        return self.pen.glyph()

def romanize(input_path, output_path):
    font = TTFont(input_path)
    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    for glyph_name in font.getGlyphOrder():
        pen = RomanPolygonPen(glyphSet)
        glyphSet[glyph_name].draw(pen)
        new_glyphs[glyph_name] = pen.getGlyph()

    font["glyf"].glyphs = new_glyphs
    if "hinting" in font: font["hinting"] = None
    if "prep" in font: del font["prep"]
    if "fpgm" in font: del font["fpgm"]
    font.save(output_path)

if __name__ == "__main__":
    romanize("SourceHanSans.ttf", "Max_Roman_Stone.ttf")
