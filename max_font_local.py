from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
from fontTools.misc.transform import Transform
from fontTools.varLib.instancer import instantiateVariableFont
import time

# 保留第一版最舒服的画笔逻辑
class MaxMediumPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        # 第一版：缩放保持 0.95，保证最佳大小和空气感
        self.transform = Transform().scale(0.95, 0.95)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt):
        x, y = self.transform.transformPoint(pt)
        self.pen.moveTo((x, y))

    def _lineTo(self, pt):
        x, y = self.transform.transformPoint(pt)
        self.pen.lineTo((x, y))

    def _curveToOne(self, pt1, pt2, pt3):
        x1, y1 = self.transform.transformPoint(pt1)
        x2, y2 = self.transform.transformPoint(pt2)
        x3, y3 = self.transform.transformPoint(pt3)
        # 第一版：切角阈值保持 3，保留温柔的锐利感
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

def build_font():
    print("📥 正在加载源字体 ...")
    font = TTFont("SourceHanSerif.ttf")

    print("⚡ 正在注入 500 瓦（wght=500）中黑字重...")
    try:
        # 调用可变字体内核，提取 Medium (500) 粗细
        font = instantiateVariableFont(font, {"wght": 500})
    except Exception:
        print("如果提取失败，回退到默认字重。")

    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"

    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    print("🔪 正在执行微创切角（保留第一版手感）...")
    start_time = time.time()
    
    count = 0
    for glyph_name in font.getGlyphOrder():
        try:
            pen = MaxMediumPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except Exception:
            pen = TTGlyphPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        
        count += 1
        if count % 10000 == 0:
            print(f"  ...已处理 {count} 个字符...")

    font["glyf"].glyphs = new_glyphs
    for glyph_name in font.getGlyphOrder():
        glyph = font["glyf"][glyph_name]
        try:
            glyph.recalcBounds(font["glyf"])
        except Exception:
            glyph.xMin = glyph.yMin = glyph.xMax = glyph.yMax = 0

    font["maxp"].recalc(font)
    
    font.save("Max_Font_V27.ttf")
    print(f"✅ 完美生成！耗时 {time.time() - start_time:.2f} 秒。文件：Max_Font_V27.ttf")

if __name__ == "__main__":
    build_font()
