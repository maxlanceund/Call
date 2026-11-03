from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

# 极简安全画笔：增加空气感（微调字面率） + 微创硬化
class MaxAiryPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        # 将每个字稍微缩小一点（比如 0.95），用来增加字与字之间的“空气感”
        self.transform = Transform().scale(0.95, 0.95)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        x, y = self.transform.transformPoint(pt)
        self.pen.moveTo((x, y))

    def _lineTo(self, pt):
        x, y = self.transform.transformPoint(pt)
        self.pen.lineTo((x, y))

    def _curveToOne(self, pt1, pt2, pt3):
        # 保留平滑曲线，但如果在极小范围内，直接拉直（微创硬化）
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

def romanize(input_path, output_path):
    print(f"加载字体: {input_path}")
    font = TTFont(input_path)
    
    # 清理可变字体表头
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    print("正在注入空气感与微创衬线...")
    for glyph_name in font.getGlyphOrder():
        try:
            pen = MaxAiryPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except Exception:
            # 绝对防崩机制：复杂的生僻字直接原样保留
            pen = TTGlyphPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()

    font["glyf"].glyphs = new_glyphs
    
    print("重新计算边界...")
    for glyph_name in font.getGlyphOrder():
        glyph = font["glyf"][glyph_name]
        try:
            glyph.recalcBounds(font["glyf"])
        except Exception:
            glyph.xMin = glyph.yMin = glyph.xMax = glyph.yMax = 0

    font["maxp"].recalc(font)
    font.save(output_path)
    print(f"✅ 生成完毕: {output_path}")

if __name__ == "__main__":
    romanize("SourceHanSerif.ttf", "Max_Font_Cloud.ttf")
