from playwright.sync_api import sync_playwright

TOP_URL = "https://www.hellowork.mhlw.go.jp/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("トップページアクセス")

    page.goto(TOP_URL)

    page.wait_for_timeout(5000)

    # 求人情報検索へ
    page.get_by_role("link", name="求人情報検索").first.click()

    page.wait_for_timeout(5000)

    print("\n===== input一覧 =====\n")

    inputs = page.locator("input")

    input_count = inputs.count()

    for i in range(input_count):
        try:
            elem = inputs.nth(i)

            input_type = elem.get_attribute("type")
            input_name = elem.get_attribute("name")
            input_id = elem.get_attribute("id")

            print("-" * 40)
            print("type:", input_type)
            print("name:", input_name)
            print("id:", input_id)

        except:
            pass

    print("\n===== button一覧 =====\n")

    buttons = page.locator("button")

    button_count = buttons.count()

    for i in range(button_count):
        try:
            text = buttons.nth(i).inner_text()

            print("-" * 40)
            print(text)

        except:
            pass

    browser.close()
