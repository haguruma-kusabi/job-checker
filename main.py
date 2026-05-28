import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://kyushoku.hellowork.mhlw.go.jp"

# ★ここは「検索結果ページURL」に差し替え
SEARCH_URL = "https://kyushoku.hellowork.mhlw.go.jp/kyushoku/GEAA110010.do"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(SEARCH_URL, headers=headers)
res.encoding = "utf-8"

soup = BeautifulSoup(res.text, "html.parser")

jobs = []

# ハロワは構造が変わるので「リンクベース」で拾うのが安定
for a in soup.find_all("a"):
    text = a.get_text(strip=True)
    href = a.get("href")

    # 求人っぽいリンクだけ残す（かなり重要なフィルタ）
    if not href:
        continue

    if "GECA" in href or "detail" in href.lower():
        full_url = urljoin(BASE_URL, href)

        if text:
            jobs.append({
                "title": text,
                "url": full_url
            })

# 重複除去（重要）
unique = []
seen = set()

for job in jobs:
    if job["url"] in seen:
        continue
    seen.add(job["url"])
    unique.append(job)

# 出力確認
print(f"取得件数: {len(unique)}")

for j in unique[:10]:
    print(j["title"])
    print(j["url"])
    print("-" * 40)
