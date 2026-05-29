from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    print("トップページアクセス")

    # =========================
    # トップページ
    # =========================
    page.goto(TOP_URL)

    page.wait_for_timeout(5000)

    # =========================
    # 求人検索へ
    # =========================
    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name="求人情報検索"
    ).first.click()

    page.wait_for_timeout(5000)

    # =========================
    # 一般求人
    # =========================
    print("一般求人チェック")

    page.check("#ID_ippanCKBox1")

    page.wait_for_timeout(1000)

    # =========================
    # フリーワード
    # =========================
    print("フリーワード入力")

    input_box = page.locator(
        'input[name="freeWordInput"]'
    )

    input_box.click()

    page.keyboard.type("エンジニア")

    page.wait_for_timeout(1000)

    print("入力値:", input_box.input_value())

    # =========================
    # 検索
    # =========================
    print("検索実行")

    page.get_by_role(
        "button",
        name="検索する"
    ).click()

    page.wait_for_timeout(10000)

    # =========================
    # URL
    # =========================
    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    # =========================
    # body
    # =========================
    body = page.locator("body").inner_text()

    print("\n===== BODY先頭3000文字 =====\n")

    print(body[:3000])

    browser.close()
