from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("トップページアクセス")

    page.goto(TOP_URL)

    page.wait_for_timeout(5000)

    # =========================
    # 求人情報検索クリック
    # =========================
    print("求人情報検索クリック")

    page.get_by_text("求人情報検索").click()

    page.wait_for_timeout(5000)

    # =========================
    # 結果確認
    # =========================
    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    html = page.content()

    print("\n===== HTML先頭1000文字 =====\n")
    print(html[:1000])

    browser.close()
