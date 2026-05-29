from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("トップページアクセス")

    page.goto(TOP_URL)

    page.wait_for_timeout(5000)

    print("\n===== 求人系リンク探索 =====\n")

    links = page.locator("a")

    count = links.count()

    for i in range(count):
        try:
            text = links.nth(i).inner_text().strip()
            href = links.nth(i).get_attribute("href")

            # ★求人系だけ表示
            if "求人" in text or "検索" in text:
                print("-" * 40)
                print("text:", text)
                print("href:", href)

        except:
            pass

    browser.close()
