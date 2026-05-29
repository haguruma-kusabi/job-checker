from playwright.sync_api import sync_playwright
import re
import time

# =========================
# スコア計算
# =========================
def calculate_score(text):
    score = 50

    plus_keywords = [
        "未経験",
        "資格不問",
        "学歴不問",
        "土日休",
        "年間休日120",
        "賞与",
        "正社員",
        "残業なし",
        "転勤なし",
        "通勤手当",
    ]

    minus_keywords = [
        "交通誘導",
        "夜勤",
        "契約社員",
        "警備員",
    ]

    for keyword in plus_keywords:
        if keyword in text:
            score += 10

    for keyword in minus_keywords:
        if keyword in text:
            score -= 10

    return max(0, min(score, 100))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("トップページアクセス")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/index.html",
        wait_until="domcontentloaded"
    )

    # =========================
    # 求人情報検索
    # =========================
    print("求人情報検索クリック")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?action=initDisp&screenId=GECA110010",
        wait_until="domcontentloaded"
    )

    # =========================
    # 一般求人
    # =========================
    print("一般求人チェック")

    page.locator('label[for="ID_ippan"]').click()

    # =========================
    # 就業場所選択
    # =========================
    print("就業場所選択")

    page.locator("#ID_todohukenHiddenAccoBtn").click()

    page.wait_for_timeout(2000)

    # =========================
    # 沖縄県選択
    # =========================
    print("沖縄選択")

    page.locator("#ID_skCheck47947").check(force=True)

    # =========================
    # 決定ボタン
    # =========================
    print("都道府県決定")

    page.locator('button:has-text("決定")').last.click()

    page.wait_for_timeout(2000)

    # =========================
    # 職種カテゴリ選択
    # =========================
    print("職種カテゴリ選択")

    # 警備・ビル等の管理
    # 実checkboxを直接操作
    page.locator("#ID_daiEasyShokusyuBox5").check(force=True)

    page.wait_for_timeout(1000)

    # =========================
    # 検索実行
    # =========================
    print("検索実行")

    search_button = page.locator("#ID_searchBtn")

    search_button.click(force=True)

    page.wait_for_timeout(5000)

    # =========================
    # 結果確認
    # =========================
    print("\n現在URL:\n")
    print(page.url)

    print("\nタイトル:\n")
    print(page.title())

    body_text = page.locator("body").inner_text()

    print("\n===== 検索結果先頭 =====\n")
    print(body_text[:3000])

    # =========================
    # 求人抽出
    # =========================
    print("\n===== スコアリング =====\n")

    pattern = r"職種\s+(.*?)\s+職種解説"

    jobs = re.findall(pattern, body_text, re.S)

    if not jobs:
        print("求人が取得できませんでした")
    else:
        for i, job in enumerate(jobs[:10], start=1):
            clean_job = " ".join(job.split())

            score = calculate_score(clean_job)

            print(f"{i}. スコア:{score}")
            print(clean_job)
            print("-" * 50)

    browser.close()
