from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("トップページアクセス")

    page.goto(TOP_URL)

    page.wait_for_timeout(5000)

    print("現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    print("\nリンク一覧取得")

    links = page.locator("a")

    count = links.count()

    print(f"リンク数: {count}")

    for i in range(min(count, 20)):
        text = links.nth(i).inner_text()
        href = links.nth(i).get_attribute("href")

        print("-" * 40)
        print("text:", text)
        print("href:", href)

    browser.close()
