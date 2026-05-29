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

    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name=re.compile("求人情報検索")
    ).click()

    page.wait_for_load_state("domcontentloaded")

    print("一般求人チェック")

    page.get_by_text("一般求人", exact=True).click()

    # =========================
    # 就業場所選択
    # =========================

    print("就業場所選択")

    page.get_by_role(
        "button",
        name=re.compile("都道府県から選択")
    ).click()

    # モーダル表示待機
    page.wait_for_timeout(2000)

    print("沖縄選択")

    # JSで直接チェック
    page.evaluate("""
        () => {
            const el = document.querySelector('#ID_skCheck47947');
            if (el) {
                el.checked = true;
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    """)

    page.wait_for_timeout(1000)

    print("都道府県決定")

    # 決定ボタン
    page.locator("button").filter(
        has_text=re.compile("決定")
    ).first.click()

    page.wait_for_timeout(2000)

    # =========================
    # 職種カテゴリ選択
    # =========================

    print("職種カテゴリ選択")

    # ラベル直接クリック
    page.locator(
        'label[for="ID_daiEasyShokusyuBox6"]'
    ).click()

    page.wait_for_timeout(1000)

    # =========================
    # フリーワード
    # =========================

    print("フリーワード入力")

    keyword_box = page.locator('input[name="freeWord"]')

    keyword_box.fill("")

    # =========================
    # 検索実行
    # =========================

    print("検索実行")

    search_button = page.locator("#ID_searchBtn")

    # force=Trueでモーダル干渉回避
    search_button.click(force=True)

    page.wait_for_load_state("domcontentloaded")

    time.sleep(5)

    # =========================
    # 結果表示
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

        if "経験不問" in job:
            score += 10

        if "資格不問" in job:
            score += 10

        if "時間外労働なし" in job:
            score += 15

        if "通勤手当あり" in job:
            score += 5

        if "転勤なし" in job:
            score += 10

        # =====================
        # タイトル抽出
        # =====================

        title = "タイトル不明"

        m = re.search(r"職種\s+([^\n]+)", job)

        if m:
            title = m.group(1).strip()

        print(f"{count+1}. スコア:{score} / {title}")

        count += 1

        if count >= 20:
            break

    browser.close()
