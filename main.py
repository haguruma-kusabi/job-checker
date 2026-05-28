import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ======================
# 設定
# ======================
BASE_URL = "https://kyushoku.hellowork.mhlw.go.jp"

# ★ここは必ず「検索結果ページURL」にすること
SEARCH_URL = "https://kyushoku.hellowork.mhlw.go.jp/kyushoku/GEAA110010.do"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ======================
# ① リクエスト取得
# ======================
res = requests.get(SEARCH_URL, headers=headers)

# 文字化け対策（ハロワはこれ重要）
res.encoding = res.apparent_encoding

html = res.text

# ======================
# ② デバッグ出力（最重要）
# ======================
print("\n===== HTML先頭2000文字 =====\n")
print(html[:2000])

print("\n===== HTML末尾1000文字 =====\n")
print(html[-1000:])

# ======================
# ③ BeautifulSoup解析
# ======================
soup = BeautifulSoup(html, "html.parser")

# ======================
# ④ 求人抽出（リンクベース）
# ======================
jobs = []

for a in soup.find_all("a"):
    text = a.get_text(strip=True)
    href = a.get("href")

    if not href:
        continue

    # ハロワ求人詳細っぽいリンクを拾う
    if "GECA" in href or "GECC" in href or "detail" in href.lower():
        full_url = urljoin(BASE_URL, href)

        if text:
            jobs.append({
                "title": text,
                "url": full_url
            })

# ======================
# ⑤ 重複除去
# ======================
unique = []
seen = set()

for job in jobs:
    if job["url"] in seen:
        continue
    seen.add(job["url"])
    unique.append(job)

# ======================
# ⑥ 結果表示
# ======================
print("\n===== 抽出結果 =====")
print(f"取得件数: {len(unique)}\n")

for j in unique[:10]:
    print("タイトル:", j["title"])
    print("URL:", j["url"])
    print("-" * 40)
