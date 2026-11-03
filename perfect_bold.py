from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
from fontTools.misc.transform import Transform
from fontTools.varLib.instancer import instantiateVariableFont
import time

# 完全照搬你第一版觉得最完美的画笔（0.95缩放，阈值3切角）
class PerfectPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.transform = Transform().scale(0.95, 0.95)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        self.pen.moveTo(self.transform.transformPoint(pt))
    def _lineTo(self, pt):
        self.pen.lineTo(self.transform.transformPoint(pt))
    def _curveToOne(self, pt1, pt2, pt3):
        x1, y1 = self.transform.transformPoint(pt1)
        x2, y2 = self.transform.transformPoint(pt2)
        x3, y3 = self.transform.transformPoint(pt3)
        if abs(x3 - x1) < 3 or abs(y3 - y1) < 3:
            self.pen.lineTo((x3, y3))
        else:
            self.pen.curveTo((x1, y1), (x2, y2), (x3, y3))
    def _qCurveToOne(self, pt1, pt2):
        x1, y1 = self.transform.transformPoint(pt1)
        x2, y2 = self.transform.transformPoint(pt2)
        if abs(x2 - x1) < 3 or abs(y2 - y1) < 3:
            self.pen.lineTo((x2, y2))
        else:
            self.pen.qCurveTo((x1, y1), (x2, y2))
    def _closePath(self):
        self.pen.closePath()
    def getGlyph(self):
        return self.pen.glyph()

font = TTFont("SourceHanSerif.ttf")
# 🎯 仅仅把字重从默认的 400，加到 480（比原来稍微粗一点）
font = instantiateVariableFont(font, {"wght": 480})

for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
    if tag in font: del font[tag]
font.sfntVersion = "\x00\x01\x00\x00"

glyphSet = font.getGlyphSet()
new_glyphs = {}
for glyph_name in font.getGlyphOrder():
    try:
        pen = PerfectPen(glyphSet)
        glyphSet[glyph_name].draw(pen)
        new_glyphs[glyph_name] = pen.getGlyph()
    except Exception:
        pen = TTGlyphPen(glyphSet)
        glyphSet[glyph_name].draw(pen)
        new_glyphs[glyph_name] = pen.getGlyph()

font["glyf"].glyphs = new_glyphs
for glyph_name in font.getGlyphOrder():
    glyph = font["glyf"][glyph_name]
    try: glyph.recalcBounds(font["glyf"])
    except: glyph.xMin = glyph.yMin = glyph.xMax = glyph.yMax = 0

font["maxp"].recalc(font)
font.save("Max_Perfect_Bold.ttf")
print("✅ 搞定！已生成：Max_Perfect_Bold.ttf")
