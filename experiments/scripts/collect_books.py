import requests, json, os, time, random, urllib3, re
urllib3.disable_warnings()

TOKEN = ""
tf = os.path.expanduser("~/.github_token")
if os.path.exists(tf):
    TOKEN = open(tf).read().strip()

UA = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36"

def h():
    x = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    if TOKEN: x["Authorization"] = f"Bearer {TOKEN}"
    return x

def req(url, params=None, timeout=10, retries=3):
    for i in range(retries):
        try:
            r = requests.get(url, params=params, headers=h(), timeout=timeout)
            if r.status_code == 200: return r
            if r.status_code == 403: time.sleep(10)
            else: return r
        except Exception:
            if i < retries-1: time.sleep(2)
    return None

def search(q):
    url = "https://api.github.com/search/repositories"
    # 每次随机取前几页，增加盲盒的随机性
    p = {"q": q, "sort": "stars", "order": "desc", "per_page": 30, "page": random.randint(1,3)}
    r = req(url, params=p)
    if not r: return []
    try: return r.json().get("items", [])
    except: return []

def is_chinese(text):
    if not text: return False
    text_lower = text.lower()
    if re.search(r'[\u4e00-\u9fa5]', text): return True
    if re.search(r'\b(zh|cn|chinese)\b', text_lower): return True
    if "-zh" in text_lower or "_zh" in text_lower: return True
    return False

def get_epub(repo_full_name):
    r = req(f"https://api.github.com/repos/{repo_full_name}/releases/latest", timeout=8, retries=2)
    if r:
        try:
            for a in r.json().get("assets", []):
                if a["name"].lower().endswith(".epub") and a["size"] > 300 * 1024:
                    return {"book_name": a["name"], "epub_url": a["browser_download_url"], "epub_size": a["size"], "is_zh": is_chinese(a["name"])}
        except: pass

    r_repo = req(f"https://api.github.com/repos/{repo_full_name}", timeout=8, retries=2)
    if not r_repo: return None
    default_branch = r_repo.json().get("default_branch", "main")

    r_tree = req(f"https://api.github.com/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1", timeout=10, retries=2)
    if r_tree:
        try:
            for item in r_tree.json().get("tree", []):
                if item["type"] == "blob" and item["path"].lower().endswith(".epub"):
                    file_size = item.get("size", 0)
                    file_path_lower = item["path"].lower()
                    if file_size > 500 * 1024: # 提高到 500KB
                        if not any(junk in file_path_lower for junk in ["test", "dummy", "example", "sample", "template"]):
                            download_url = f"https://raw.githubusercontent.com/{repo_full_name}/{default_branch}/{item['path']}"
                            book_name = item["path"].split("/")[-1]
                            is_zh = is_chinese(item['path']) or is_chinese(book_name)
                            return {"book_name": book_name, "epub_url": download_url, "epub_size": file_size, "is_zh": is_zh}
        except: pass
    return None

def save(new):
    os.makedirs("data", exist_ok=True)
    path = "data/random_books.json"
    old = []
    if os.path.exists(path):
        try: old = json.load(open(path))
        except: old = []
    m = {}
    for r in old + new: m[r["name"]] = r
    result = list(m.values())
    json.dump(result, open(path, "w"), ensure_ascii=False, indent=2)
    return len(result)

def main():
    # 🔥 核心改动：使用 GitHub 的 topic 标签和经典书库名
    BQ = [
        "topic:epub", 
        "topic:ebooks", 
        "topic:books", 
        "free-programming-books", 
        "zlib", 
        "awesome books"
    ]
    
    books, seen, cnt = [], set(), 0
    for q in BQ:
        if cnt >= 20: break
        try:
            for it in search(q):
                if cnt >= 20: break
                if it["full_name"] in seen: continue
                
                print(f"正在检查: {it['full_name']} ...")
                epub = get_epub(it["full_name"])
                
                if epub:
                    seen.add(it["full_name"])
                    zh_tag = "🇨🇳[中文]" if epub.get("is_zh") else "🌍[外文]"
                    
                    books.append({
                        "name": it["full_name"], 
                        "description": it.get("description") or "无描述",
                        "url": it["html_url"], 
                        "stars": it["stargazers_count"],
                        "language": it.get("language") or "未知", 
                        "keyword": q,
                        "book_name": epub["book_name"], 
                        "epub_url": epub["epub_url"], 
                        "epub_size": epub["epub_size"],
                        "is_chinese": epub.get("is_zh", False)
                    })
                    cnt += 1
                    size_mb = epub['epub_size'] / 1024 / 1024
                    print(f"  ✅ [{cnt}/20] 找到: {zh_tag} {epub['book_name']} ({size_mb:.1f} MB)")
            save(books) 
        except Exception as e:
            print(f"搜索 {q} 失败: {e}")
    total = save(books)
    print(f"\n本次新抓 {len(books)} 本书，书库现有 {total} 本书")

if __name__ == "__main__":
    main()
