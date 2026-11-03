import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen

# 自定义一个画笔：强制把所有曲线变成直线（刀凿斧刻感）
class RomanPolygonPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        self.pen.moveTo(pt)

    def _lineTo(self, pt):
        self.pen.lineTo(pt)

    def _curveToOne(self, pt1, pt2, pt3):
        # 核心魔法：无视控制点，直接用直线连到终点
        self.pen.lineTo(pt3)

    def _qCurveToOne(self, pt1, pt2):
        self.pen.lineTo(pt2)

    def _closePath(self):
        self.pen.closePath()

    def getGlyph(self):
        return self.pen.glyph()

def romanize(input_path, output_path):
    print(f"正在加载原始字体: {input_path}")
    font = TTFont(input_path)
    glyphSet = font.getGlyphSet()
    
    print("正在把所有曲线切割成硬朗的直线...")
    new_glyphs = {}
    for glyph_name in font.getGlyphOrder():
        pen = RomanPolygonPen(glyphSet)
        glyphSet[glyph_name].draw(pen)
        new_glyphs[glyph_name] = pen.getGlyph()

    # 替换旧字形，并去掉 Hinting（因为几何变了，旧的 hinting 会报错）
    print("正在重组字体...")
    font["glyf"].glyphs = new_glyphs
    if "hinting" in font:
        font["hinting"] = None
    if "prep" in font:
        del font["prep"]
    if "fpgm" in font:
        del font["fpgm"]

    print(f"保存罗马风字体至: {output_path}")
    font.save(output_path)
    print("✅ 字体生成完毕！")

if __name__ == "__main__":
    # 我们指定输入和输出
    # 使用思源黑体（Noto Sans CJK）作为基础字体，它的结构最稳定
    input_font = "SourceHanSans.ttf" 
    output_font = "Max_Roman_Stone.ttf"
    romanize(input_font, output_font)
