from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
from fontTools.varLib.instancer import instantiateVariableFont
import time

# 极度冷血的几何画笔：只要看到曲线，直接切断变成直角折线！
class LowPolyPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt): self.pen.moveTo(pt)
    def _lineTo(self, pt): self.pen.lineTo(pt)
    
    def _curveToOne(self, pt1, pt2, pt3):
        # 暴力几何化：取控制点和终点的中间点，直接画两根直线
        mid_x = (pt1[0] + pt3[0]) / 2
        mid_y = (pt1[1] + pt3[1]) / 2
        self.pen.lineTo((mid_x, mid_y))
        self.pen.lineTo(pt3)

    def _qCurveToOne(self, pt1, pt2):
        # 二次曲线也一样，全部砍成直线折角
        self.pen.lineTo(pt2)

    def _closePath(self): self.pen.closePath()
    def getGlyph(self): return self.pen.glyph()

def build():
    print("📥 正在加载底包...")
    font = TTFont("SourceHanSerif.ttf")
    
    print("📐 提取 430 字重（几何化会显粗，所以降一点字重）...")
    font = instantiateVariableFont(font, {"wght": 430})
    
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    print("🔪 正在执行低多边形几何切割...")
    start_time = time.time()
    
    for glyph_name in font.getGlyphOrder():
        try:
            pen = LowPolyPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except Exception:
            # 复杂汉字切坏了就直接保留原样，防止糊成一团
            pen = TTGlyphPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()

    font["glyf"].glyphs = new_glyphs
    
    print("🧩 保存中...")
    font.save("Max_Geometry.ttf")
    print(f"✅ 生成完毕！耗时 {time.time() - start_time:.2f} 秒。文件：Max_Geometry.ttf")

if __name__ == "__main__":
    build()
