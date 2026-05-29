from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    print("トップページアクセス")

    # =========================
    # トップ
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
    # 一般求人チェック
    # =========================
    print("一般求人チェック")

    page.check("#ID_ippanCKBox1")

    page.wait_for_timeout(1000)

    # =========================
    # フリーワード入力
    # =========================
    print("フリーワード入力")

    input_box = page.locator('input[name="freeWordInput"]')

    input_box.click()

    page.keyboard.type("Python")

    page.wait_for_timeout(1000)

    # 入力確認
    value = input_box.input_value()

    print("入力値:", value)

    # =========================
    # 検索ボタンクリック
    # =========================
    print("検索実行")

    page.get_by_role(
        "button",
        name="検索する"
    ).click()

    page.wait_for_timeout(10000)

    # =========================
    # 現在URL
    # =========================
    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    # =========================
    # body確認
    # =========================
    body = page.locator("body").inner_text()

    print("\n===== BODY先頭2000文字 =====\n")

    print(body[:2000])

    browser.close()
