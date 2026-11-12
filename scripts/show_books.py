import json
import os

path = "data/random_books.json"
if not os.path.exists(path):
    print("❌ 书库是空的，先去抓书吧！")
    exit()

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 排个序：中文书优先，然后按文件大小从大到小排
data.sort(key=lambda x: (x.get("is_chinese", False), x.get("epub_size", 0)), reverse=True)

print(f"📚 你的赛博书库总览 (共 {len(data)} 本)\n" + "="*55)

for i, b in enumerate(data, 1):
    zh_tag = "🇨🇳[中文]" if b.get("is_chinese") else "🌍[外文]"
    size_mb = b.get("epub_size", 0) / 1024 / 1024
    name = b.get("book_name", "未知书名")
    repo = b.get("name", "未知仓库")
    url = b.get("url", "")
    
    print(f"{i:02d}. {zh_tag} {name}")
    print(f"    📦 大小: {size_mb:.2f} MB")
    print(f"    📂 来源: {repo}")
    print(f"    🔗 链接: {url}")
    print("-" * 55)
