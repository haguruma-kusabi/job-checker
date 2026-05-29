from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("トップページアクセス")

    # =========================
    # トップページ
    # =========================
    page.goto(TOP_URL)

    page.wait_for_timeout(5000)

    # =========================
    # 求人情報検索へ
    # =========================
    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name="求人情報検索"
    ).first.click()

    page.wait_for_timeout(5000)

    # =========================
    # フリーワード入力
    # =========================
    print("フリーワード入力")

    page.fill(
        'input[name="freeWordInput"]',
        "Python"
    )

    page.wait_for_timeout(2000)

    # =========================
    # 検索実行
    # =========================
    print("検索実行")

    page.click('#ID_searchShosaiBtn')

    page.wait_for_timeout(8000)

    # =========================
    # 結果確認
    # =========================
    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    print("\n===== 検索結果HTML先頭1000文字 =====\n")

    html = page.content()

    print(html[:1000])

    # =========================
    # 求人タイトル候補抽出
    # =========================
    print("\n===== 求人タイトル候補 =====\n")

    links = page.locator("a")

    count = links.count()

    for i in range(count):
        try:
            text = links.nth(i).inner_text().strip()

            if len(text) > 10:
                print(text)

        except:
            pass

    browser.close()
