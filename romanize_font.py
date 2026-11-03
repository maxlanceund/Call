from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
import math

class ElegantRomanPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        self.pen.moveTo(pt)

    def _lineTo(self, pt):
        self.pen.lineTo(pt)

    def _curveToOne(self, pt1, pt2, pt3):
        # 核心微创逻辑：保留曲线的主体，但在终点附近强行拉一段极短的直线，造出“切角/衬线”
        # 计算终点前的一小段距离
        dx = pt3[0] - pt2[0]
        dy = pt3[1] - pt2[1]
        length = math.hypot(dx, dy)
        
        if length > 10: # 如果线段足够长，才加切角，防止小字糊掉
            # 往回缩一小段距离作为切点（根据字的大小动态调整，这里暂定 5 个单位）
            cut_len = 5 
            ratio = cut_len / length
            cut_x = pt3[0] - dx * ratio
            cut_y = pt3[1] - dy * ratio
            # 曲线走到切点，然后一刀切直线连到终点
            self.pen.curveTo(pt1, pt2, (cut_x, cut_y))
            self.pen.lineTo(pt3)
        else:
            self.pen.curveTo(pt1, pt2, pt3)

    def _qCurveToOne(self, pt1, pt2):
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]
        length = math.hypot(dx, dy)
        if length > 10:
            cut_len = 5 
            ratio = cut_len / length
            cut_x = pt2[0] - dx * ratio
            cut_y = pt2[1] - dy * ratio
            self.pen.qCurveTo(pt1, (cut_x, cut_y))
            self.pen.lineTo(pt2)
        else:
            self.pen.qCurveTo(pt1, pt2)

    def _closePath(self):
        self.pen.closePath()

    def getGlyph(self):
        return self.pen.glyph()

def romanize(input_path, output_path):
    print(f"加载字体: {input_path}")
    font = TTFont(input_path)
    
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    print("正在对复杂汉字进行微创切角...")
    for glyph_name in font.getGlyphOrder():
        try:
            pen = ElegantRomanPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except:
            new_glyphs[glyph_name] = TTGlyphPen(glyphSet).glyph()

    font["glyf"].glyphs = new_glyphs
    
    for glyph_name in font.getGlyphOrder():
        glyph = font["glyf"][glyph_name]
        try:
            glyph.recalcBounds(font["glyf"])
        except:
            glyph.xMin = glyph.yMin = glyph.xMax = glyph.yMax = 0

    font["maxp"].recalc(font)
    font.save(output_path)
    print(f"✅ 生成完毕: {output_path}")

if __name__ == "__main__":
    romanize("SourceHanSerif.ttf", "Max_Roman_Reading.ttf")
