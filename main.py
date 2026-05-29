from playwright.sync_api import sync_playwright
import time

KEYWORD = "エンジニア"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("トップページアクセス")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/",
        wait_until="networkidle"
    )

    # 求人情報検索クリック
    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name="求人情報検索"
    ).first.click()

    page.wait_for_load_state("networkidle")

    # 一般求人チェック
    print("一般求人チェック")

    page.locator("#ID_ippanCKBox1").check()

    # フリーワード入力
    print("フリーワード入力")
    print(f"入力値: {KEYWORD}")

    page.locator("#ID_freeWordInput").fill(KEYWORD)

    # 検索実行
    print("検索実行")

    page.locator("#ID_searchShosaiBtn").click()

    # 検索結果待機
    page.wait_for_timeout(5000)

    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    body = page.locator("body").inner_text()

    if "検索結果" in body:
        print("\n検索成功")

        # 求人タイトル取得
        jobs = page.locator("text=職種").all()

        print(f"\n取得件数: {len(jobs)}")

        # 職種ラベル周辺を取得
        text = body.split("検索結果")[-1]

        print("\n===== 検索結果先頭 =====\n")
        print(text[:5000])

    else:
        print("\n検索失敗")
        print(body[:3000])

    browser.close()
