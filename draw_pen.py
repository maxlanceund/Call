from PIL import Image, ImageDraw

# 创建 256x256 的透明画布
img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 颜色设为纯白
WHITE = (255, 255, 255, 255)

# 1. 画笔杆 (从右上到左下的粗直线)
draw.line([(180, 60), (50, 200)], fill=WHITE, width=8)

# 2. 画笔尖 (左下方的小多边形，形成削尖的效果)
draw.polygon([(50, 200), (30, 220), (60, 210)], fill=WHITE)

# 3. 画羽毛的主体 (右上角，使用多边形拼接出羽毛优美的弧度)
# 这是羽毛的上半部分
draw.polygon([(180, 60), (220, 30), (160, 100), (120, 120)], fill=WHITE)
# 这是羽毛的下半部分
draw.polygon([(180, 60), (210, 90), (140, 160), (90, 160)], fill=WHITE)

# 4. 画羽毛中间的轴线 (增加一点细节)
draw.line([(190, 50), (100, 150)], fill=(0,0,0,0), width=2) # 镂空一条线

# 稍微加一点羽毛的纹理线（用小线条划开）
draw.line([(160, 100), (130, 130)], fill=(0,0,0,0), width=3)
draw.line([(140, 160), (110, 140)], fill=(0,0,0,0), width=3)

# 保存为 my_pen.png
img.save('my_pen.png')
print("羽毛笔 my_pen.png 绘制完成！")
