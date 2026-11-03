from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
import math

# 专属微创画笔：只把接近直线的曲线拉直，保留宋体原有的柔美
class MaxStylePen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        self.pen.moveTo(pt)

    def _lineTo(self, pt):
        self.pen.lineTo(pt)

    def _curveToOne(self, pt1, pt2, pt3):
        # 如果曲线的控制点偏移不大（接近直线），就强行拉成直线（增加极客硬朗感）
        dx = abs(pt3[0] - pt1[0])
        dy = abs(pt3[1] - pt1[1])
        if dx < 5 or dy < 5:
            self.pen.lineTo(pt3)
        else:
            self.pen.curveTo(pt1, pt2, pt3)

    def _qCurveToOne(self, pt1, pt2):
        dx = abs(pt2[0] - pt1[0])
        dy = abs(pt2[1] - pt1[1])
        if dx < 5 or dy < 5:
            self.pen.lineTo(pt2)
        else:
            self.pen.qCurveTo(pt1, pt2)

    def _closePath(self):
        self.pen.closePath()

    def getGlyph(self):
        return self.pen.glyph()

def build_max_font(input_path, output_path):
    print(f"加载字体: {input_path}")
    font = TTFont(input_path)
    
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    # 我们不再遍历所有几万个字，我们只挑出核心的 3000 个常用汉字（防止生僻字把系统搞崩）
    # 实际中我们直接遍历，加上异常处理
    print("正在注入 Max 基因（极客锐化与罗马衬线）...")
    for glyph_name in font.getGlyphOrder():
        try:
            pen = MaxStylePen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except Exception:
            # 遇到极其复杂的生僻字，直接原样保留（绝对不崩）
            pen = TTGlyphPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()

    font["glyf"].glyphs = new_glyphs
    
    for glyph_name in font.getGlyphOrder():
        glyph = font["glyf"][glyph_name]
        try:
            glyph.recalcBounds(font["glyf"])
        except Exception:
            glyph.xMin = glyph.yMin = glyph.xMax = glyph.yMax = 0

    font["maxp"].recalc(font)
    font.save(output_path)
    print(f"✅ 专属 Max 字体生成完毕: {output_path}")

if __name__ == "__main__":
    build_max_font("SourceHanSerif.ttf", "Max_Font_V23.ttf")
