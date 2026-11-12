import json
import os
import random
import requests
import sys

BOOKS_FILE = os.path.expanduser("~/github-random/data/random_books.json")
BOOK_DIR = "/sdcard/Download/books"

if not os.path.exists(BOOKS_FILE):
    print("❌ 书库是空的，先运行抓取脚本！")
    exit()

with open(BOOKS_FILE, "r", encoding="utf-8") as f:
    books = json.load(f)

# 如果输入了参数（书名或序号），就精准查找；否则随机抽
if len(sys.argv) > 1:
    query = sys.argv[1]
    if query.isdigit():
        # 如果输入的是数字，就按 show_books.py 里的序号找
        idx = int(query) - 1
        if 0 <= idx < len(books):
            book = books[idx]
        else:
            print("❌ 序号超出范围！")
            exit()
    else:
        # 如果输入的是文字，就模糊匹配书名
        matched = [b for b in books if query.lower() in b["book_name"].lower()]
        if not matched:
            print(f"❌ 没找到包含 '{query}' 的书")
            exit()
        book = matched[0]
else:
    book = random.choice(books)

filename = book["book_name"]
url = book["epub_url"]
out_path = os.path.join(BOOK_DIR, filename)

print("==========================================")
print("📖 准备下载书籍")
print(f"书名: {filename}")
print(f"大小: {book.get('epub_size', 0) / 1024 / 1024:.2f} MB")
print("==========================================")

os.makedirs(BOOK_DIR, exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}

try:
    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\r进度: {pct}% ({downloaded//1024//1024}MB / {total//1024//1024}MB)", end="")
        print(f"\n✅ 下载完成！保存在: {out_path}")
except Exception as e:
    print(f"\n❌ 下载失败: {e}")
