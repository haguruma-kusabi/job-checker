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
    # 求人情報検索
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

    page.check('#ID_ippanCKBox1')

    page.wait_for_timeout(1000)

    # =========================
    # フリーワード
    # =========================
    print("フリーワード入力")

    page.fill(
        'input[name="freeWordInput"]',
        "Python"
    )

    page.wait_for_timeout(1000)

    # =========================
    # 検索実行
    # =========================
    print("検索実行")

    page.click('#ID_searchShosaiBtn')

    page.wait_for_timeout(10000)

    # =========================
    # URL確認
    # =========================
    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    # =========================
    # エラーメッセージ確認
    # =========================
    print("\n===== bodyテキスト先頭 =====\n")

    body_text = page.locator("body").inner_text()

    print(body_text[:3000])

    browser.close()
