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
        # 核心魔法：无视控制点，直接用直线连到终点（模拟刀刻感）
        self.pen.lineTo(pt3)

    def _qCurveToOne(self, pt1, pt2):
        self.pen.lineTo(pt2)

    def _closePath(self):
        self.pen.closePath()

    def getGlyph(self):
        return self.pen.glyph()

def romanize(input_path, output_path):
    print(f"加载字体: {input_path}")
    font = TTFont(input_path)
    
    # 暴力清洗：如果是可变字体，强行删掉它的可变表，防止保存冲突
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT"]:
        if tag in font:
            del font[tag]
            
    # 暴力清洗：强行把表头改回纯正 TTF，删掉可能残留的 CFF 表
    font.sfntVersion = "\x00\x01\x00\x00"
    if "CFF " in font:
        del font["CFF "]

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    print("正在切割笔画...")
    for glyph_name in font.getGlyphOrder():
        try:
            pen = RomanPolygonPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except Exception as e:
            # 如果某个字符切坏了，直接塞一个空字形，防止整个程序崩溃
            new_glyphs[glyph_name] = TTGlyphPen(glyphSet).glyph()

    print("重组字体数据...")
    font["glyf"].glyphs = new_glyphs
    font["maxp"].recalc(font)
    
    # 重新计算所有字形的边界（防止出现0宽度的错误）
    for glyph_name in font.getGlyphOrder():
        font["glyf"][glyph_name].recalcBounds(font["glyf"])

    print(f"保存为: {output_path}")
    font.save(output_path)
    print("✅ 生成完毕！")

if __name__ == "__main__":
    romanize("SourceHanSans.ttf", "Max_Roman_Stone.ttf")
