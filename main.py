from playwright.sync_api import sync_playwright
import time
import re

KEYWORD = "警備"
TARGET_PREF = "沖縄県"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("トップページアクセス")
    page.goto(
        "https://www.hellowork.mhlw.go.jp/",
        wait_until="domcontentloaded"
    )

    # 求人情報検索へ
    print("求人情報検索クリック")
    page.get_by_role("link", name=re.compile("求人情報検索")).click()

    page.wait_for_load_state("domcontentloaded")

    # 一般求人
    print("一般求人チェック")
    page.get_by_label("一般求人").check(force=True)

    # -----------------------------
    # 就業場所選択
    # -----------------------------
    print("就業場所選択")

    page.get_by_role(
        "button",
        name=re.compile("都道府県から選択")
    ).click()

    # モーダル表示待ち
    page.wait_for_timeout(3000)

    print("沖縄選択")

    # hiddenなので JS で直接チェック
    page.evaluate("""
        () => {
            const checkbox = document.querySelector('#ID_skCheck47947');
            if (checkbox) {
                checkbox.checked = true;

                checkbox.dispatchEvent(
                    new Event('change', { bubbles: true })
                );

                checkbox.dispatchEvent(
                    new Event('click', { bubbles: true })
                );
            }
        }
    """)

    page.wait_for_timeout(1000)

    # 決定ボタン
    print("都道府県決定")

    page.get_by_role(
        "button",
        name=re.compile("決定|OK")
    ).click()

    page.wait_for_timeout(2000)

    # -----------------------------
    # 職種カテゴリ
    # -----------------------------
    print("職種カテゴリ選択")

    page.get_by_text("IT・Web・エンジニア").click()

    page.wait_for_timeout(1000)

    # -----------------------------
    # フリーワード
    # -----------------------------
    print("フリーワード入力")

    keyword_box = page.locator('input[name="freeWord"]')

    if keyword_box.count() > 0:
        keyword_box.first.fill(KEYWORD)

    # -----------------------------
    # 検索実行
    # -----------------------------
    print("検索実行")

    page.get_by_role(
        "button",
        name=re.compile("検索する")
    ).click()

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(5000)

    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    body = page.locator("body").inner_text()

    print("\n===== 検索結果先頭 =====\n")
    print(body[:5000])

    # -----------------------------
    # 求人スコアリング
    # -----------------------------
    print("\n===== スコアリング =====\n")

    jobs = body.split("詳細を表示")

    scored_jobs = []

    for job in jobs:
        score = 0

        if "土日休" in job:
            score += 20

        if "年間休日数：120日" in job:
            score += 20

        if "経験不問" in job:
            score += 15

        if "資格不問" in job:
            score += 10

        if "正社員" in job:
            score += 15

        if "転勤なし" in job:
            score += 10

        if "通勤手当あり" in job:
            score += 5

        if "オンライン自主応募可" in job:
            score += 5

        title_match = re.search(r"職種\\s+(.*)", job)

        title = (
            title_match.group(1).strip()
            if title_match else "タイトル取得失敗"
        )

        scored_jobs.append({
            "title": title,
            "score": score
        })

    scored_jobs = sorted(
        scored_jobs,
        key=lambda x: x["score"],
        reverse=True
    )

    for i, job in enumerate(scored_jobs[:10], start=1):
        print(
            f"{i}. スコア:{job['score']} / {job['title']}"
        )

    browser.close()
