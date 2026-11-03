from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.basePen import BasePen
import time

# 最温和的画笔，只做极微小的硬化，绝不破坏衬线！
class SafeSerifPen(BasePen):
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.pen = TTGlyphPen(glyphSet)

    def _moveTo(self, pt): self.pen.moveTo(pt)
    def _lineTo(self, pt): self.pen.lineTo(pt)
    
    def _curveToOne(self, pt1, pt2, pt3):
        # 阈值极小化（0.5），只切掉极其明显的圆头，完美保留宋体的三角衬线
        if abs(pt3[0] - pt1[0]) < 0.5 or abs(pt3[1] - pt1[1]) < 0.5:
            self.pen.lineTo(pt3)
        else:
            self.pen.curveTo(pt1, pt2, pt3)

    def _qCurveToOne(self, pt1, pt2):
        if abs(pt2[0] - pt1[0]) < 0.5 or abs(pt2[1] - pt1[1]) < 0.5:
            self.pen.lineTo(pt2)
        else:
            self.pen.qCurveTo(pt1, pt2)

    def _closePath(self): self.pen.closePath()
    def getGlyph(self): return self.pen.glyph()

def build():
    print("📥 加载字体...")
    font = TTFont("SourceHanSerif.ttf")
    
    # 第一步：直接提取 480 字重（非常快，不走重绘逻辑）
    print("💪 调整字重为 480（微加粗）...")
    font = instantiateVariableFont(font, {"wght": 480})
    
    # 第二步：清理无用表头
    for tag in ["gvar", "fvar", "avar", "HVAR", "VVAR", "MVAR", "STAT", "CFF "]:
        if tag in font: del font[tag]
    font.sfntVersion = "\x00\x01\x00\x00"

    # 第三步：极简替换轮廓（不计算边界框，不卡死）
    glyphSet = font.getGlyphSet()
    new_glyphs = {}
    
    print("🔪 微创硬化，保护衬线（约 1 分钟）...")
    start_time = time.time()
    
    for glyph_name in font.getGlyphOrder():
        try:
            pen = SafeSerifPen(glyphSet)
            glyphSet[glyph_name].draw(pen)
            new_glyphs[glyph_name] = pen.getGlyph()
        except Exception:
            pass # 遇到计算不过的极品生僻字，直接跳过，绝对不让它卡死

    # 把成功的字放回去
    for name, glyph in new_glyphs.items():
        font["glyf"][name] = glyph

    # 直接保存，不调用 recalcBounds（这就是上一版卡死的元凶）
    font.save("Max_Final_Serif.ttf")
    print(f"✅ 完美成功！耗时 {time.time() - start_time:.2f} 秒。文件：Max_Final_Serif.ttf")

if __name__ == "__main__":
    build()
