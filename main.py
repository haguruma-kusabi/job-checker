from playwright.sync_api import sync_playwright
import re


def calc_score(text):
    score = 0

    # 加点
    if "正社員" in text:
        score += 20

    if "未経験" in text:
        score += 15

    if "経験不問" in text:
        score += 15

    if "資格不問" in text:
        score += 10

    if "週休二日制" in text:
        score += 10

    if "土日休" in text:
        score += 10

    if "年間休日数：120日" in text:
        score += 15

    if "年間休日数：121日" in text:
        score += 15

    if "年間休日数：122日" in text:
        score += 15

    if "年間休日数：123日" in text:
        score += 15

    if "転勤なし" in text:
        score += 10

    if "残業なし" in text:
        score += 10

    if "賞与" in text:
        score += 5

    if "通勤手当あり" in text:
        score += 5

    if "マイカー通勤可" in text:
        score += 5

    # 減点
    if "夜勤" in text:
        score -= 10

    if "交代制" in text:
        score -= 10

    if "シフト制" in text:
        score -= 5

    return score


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    print("トップページアクセス")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/",
        wait_until="networkidle"
    )

    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name=re.compile("求人情報検索")
    ).click()

    page.wait_for_load_state("networkidle")

    print("一般求人チェック")

    page.get_by_text(
        "一般求人",
        exact=True
    ).click()

    # =========================
    # 就業場所設定
    # =========================

    print("就業場所選択")

    page.get_by_role(
        "button",
        name="都道府県から選択"
    ).click()

    # モーダル生成待ち
    page.wait_for_timeout(3000)

    print("沖縄選択")

    # hidden checkbox を force click
    page.locator(
        "#ID_skCheck47947"
    ).click(force=True)

    page.wait_for_timeout(1000)

    print("選択ボタンクリック")

    page.get_by_role(
        "button",
        name="選択"
    ).click()

    page.wait_for_timeout(3000)

    # =========================
    # 職種カテゴリ設定
    # =========================

    print("職種カテゴリ選択")

    page.get_by_text(
        "警備・ビル等の管理",
        exact=True
    ).click()

    page.wait_for_timeout(1000)

    # =========================
    # 検索実行
    # =========================

    print("検索実行")

    page.get_by_role(
        "button",
        name="検索する"
    ).click()

    page.wait_for_load_state("networkidle")

    print("検索結果取得")

    body = page.locator("body").inner_text()

    print()
    print("===== 検索結果 =====")
    print()

    jobs = body.split("詳細を表示")

    results = []

    for job in jobs:

        if "職種" not in job:
            continue

        score = calc_score(job)

        title_match = re.search(
            r"職種\s+(.*?)\n",
            job
        )

        salary_match = re.search(
            r"([\d,]+円〜[\d,]+円)",
            job
        )

        holiday_match = re.search(
            r"年間休日数：(\d+)日",
            job
        )

        company_match = re.search(
            r"事業所名\s+(.*?)\n",
            job
        )

        place_match = re.search(
            r"就業場所\s+(.*?)\n",
            job
        )

        title = (
            title_match.group(1)
            if title_match
            else "タイトル不明"
        )

        salary = (
            salary_match.group(1)
            if salary_match
            else "給与不明"
        )

        holiday = (
            holiday_match.group(1) + "日"
            if holiday_match
            else "記載なし"
        )

        company = (
            company_match.group(1)
            if company_match
            else "事業所不明"
        )

        place = (
            place_match.group(1)
            if place_match
            else "勤務地不明"
        )

        results.append({
            "score": score,
            "title": title,
            "salary": salary,
            "holiday": holiday,
            "company": company,
            "place": place
        })

    # スコア順ソート
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    print("===== スコア順求人一覧 =====")

    for i, r in enumerate(results[:20], start=1):

        print()

        print(f"順位: {i}")
        print(f"スコア: {r['score']}")
        print(f"職種: {r['title']}")
        print(f"会社: {r['company']}")
        print(f"勤務地: {r['place']}")
        print(f"給与: {r['salary']}")
        print(f"年間休日: {r['holiday']}")

    browser.close()
