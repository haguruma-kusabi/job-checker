from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://kyushoku.hellowork.mhlw.go.jp/kyushoku/GEAA110010.do"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("ページアクセス開始")

    page.goto(URL)

    # 少し待つ（重要）
    page.wait_for_timeout(5000)

    html = page.content()

    print("\n===== HTML先頭1000文字 =====\n")
    print(html[:1000])

    soup = BeautifulSoup(html, "html.parser")

    print("\n===== title =====")
    print(soup.title.text)

    browser.close()
