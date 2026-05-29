from playwright.sync_api import sync_playwright
import re
import time

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("トップページアクセス")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/",
        wait_until="domcontentloaded"
    )

    # =========================
    # 求人検索
    # =========================

    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name=re.compile("求人情報検索")
    ).click()

    page.wait_for_load_state("domcontentloaded")

    # =========================
    # 一般求人
    # =========================

    print("一般求人チェック")

    page.get_by_text(
        "一般求人",
        exact=True
    ).click()

    page.wait_for_timeout(1000)

    # =========================
    # 沖縄選択
    # =========================

    print("就業場所選択")

    page.get_by_role(
        "button",
        name=re.compile("都道府県から選択")
    ).click()

    page.wait_for_timeout(2000)

    print("沖縄選択")

    page.evaluate("""
    () => {

        const checkbox =
            document.querySelector('#ID_skCheck47947');

        if (checkbox) {

            checkbox.checked = true;

            checkbox.dispatchEvent(
                new Event('change', { bubbles: true })
            );
        }
    }
    """)

    page.wait_for_timeout(1000)

    print("都道府県決定")

    page.locator("button").filter(
        has_text=re.compile("決定")
    ).first.click(force=True)

    page.wait_for_timeout(2000)

    # =========================
    # 職種カテゴリ
    # =========================

    print("職種カテゴリ選択")

    page.evaluate("""
    () => {

        const labels = document.querySelectorAll("label");

        for (const label of labels) {

            if (
                label.innerText.includes(
                    "警備・ビル等の管理"
                )
            ) {

                label.click();
                break;
            }
        }
    }
    """)

    page.wait_for_timeout(2000)

    # =========================
    # 検索
    # =========================

    print("検索実行")

    page.locator(
        "#ID_searchBtn"
    ).click(force=True)

    page.wait_for_load_state("domcontentloaded")

    time.sleep(5)

    # =========================
    # 結果確認
    # =========================

    print("")
    print("現在URL:")
    print(page.url)

    print("")
    print("タイトル:")
    print(page.title())

    body = page.locator("body").inner_text()

    print("")
    print("===== 検索結果先頭 =====")
    print("")
    print(body[:5000])

    # =========================
    # 求人抽出
    # =========================

    print("")
    print("===== スコアリング =====")
    print("")

    jobs = body.split("求人番号")

    count = 0

    for job in jobs:

        if "事業所名" not in job:
            continue

        score = 0

        # =====================
        # 加点条件
        # =====================

        if "正社員" in job:
            score += 20

        if "土日" in job:
            score += 15

        if "年間休日数：120日" in job:
            score += 20
