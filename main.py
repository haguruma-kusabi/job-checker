from playwright.sync_api import sync_playwright
import re
import time

# =========================
# 設定
# =========================

AREA = "沖縄"
CATEGORY = "警備・ビル等の管理"

# =========================
# スコア計算
# =========================

def calc_score(job):

    score = 0

    text = (
        job["title"]
        + job["description"]
        + job["holiday"]
        + job["tags"]
    )

    # 雇用形態
    if "正社員" in job["employment"]:
        score += 30

    # 土日休み
    if "土日" in text:
        score += 20

    # 年休120日以上
    holiday_match = re.search(r"年間休日数：(\d+)日", text)

    if holiday_match:
        holiday_num = int(holiday_match.group(1))

        if holiday_num >= 120:
            score += 20

    # 未経験歓迎
    if "経験不問" in text:
        score += 15

    # 転勤なし
    if "転勤なし" in text:
        score += 15

    # 通勤手当
    if "通勤手当あり" in text:
        score += 5

    # 夜勤減点
    if "夜勤" in text:
        score -= 10

    return score


# =========================
# メイン処理
# =========================

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

    # =========================
    # 求人検索へ
    # =========================

    print("求人情報検索クリック")

    page.get_by_role(
        "link",
        name="求人情報検索"
    ).first.click()

    page.wait_for_load_state("networkidle")

    # =========================
    # 一般求人
    # =========================

    print("一般求人チェック")

    page.locator("#ID_ippanCKBox1").check()
    
    # =========================
    # 就業場所
    # =========================

    print("就業場所選択")

    page.locator("#ID_todohukenHiddenAccoBtn").click()

    page.wait_for_timeout(2000)

    print("沖縄選択")

    page.get_by_text("沖縄県").click()

    page.wait_for_timeout(1000)

    # 決定
    page.get_by_role(
        "button",
        name="決定"
    ).click()

    page.wait_for_timeout(2000)

    # =========================
    # 職種カテゴリ
    # =========================

    print("職種カテゴリ選択")
    # =========================
    # 職種カテゴリ
    # =========================

    print("職種カテゴリ選択")

    page.get_by_text(CATEGORY).click()

    page.wait_for_timeout(2000)

    # =========================
    # 検索
    # =========================

    print("検索実行")

    page.locator("#ID_searchShosaiBtn").click()

    page.wait_for_timeout(5000)

    print("\n現在URL:")
    print(page.url)

    print("\nタイトル:")
    print(page.title())

    body = page.locator("body").inner_text()

    if "検索結果" not in body:

        print("\n検索失敗")
        print(body[:3000])

        browser.close()
        exit()

    print("\n検索成功")

    # =========================
    # 求人解析
    # =========================

    print("\n求人解析開始")

    jobs = []

    # 求人ブロック取得
    blocks = body.split("詳細を表示")

    for block in blocks:

        try:

            # 職種
            title_match = re.search(
                r"職種\s+(.+?)\s+職種解説",
                block,
                re.DOTALL
            )

            title = (
                title_match.group(1).strip()
                if title_match
                else ""
            )

            # 事業所名
            company_match = re.search(
                r"事業所名\s+(.+?)\s+就業場所",
                block,
                re.DOTALL
            )

            company = (
                company_match.group(1).strip()
                if company_match
                else ""
            )

            # 就業場所
            location_match = re.search(
                r"就業場所\s+(.+?)\s+賃金",
                block,
                re.DOTALL
            )

            location = (
                location_match.group(1).strip()
                if location_match
                else ""
            )

            # 賃金
            salary_match = re.search(
                r"賃金.*?\s+([\d,]+円〜[\d,]+円)",
                block,
                re.DOTALL
            )

            salary = (
                salary_match.group(1).strip()
                if salary_match
                else ""
            )

            # 雇用形態
            employment = ""

            if "正社員" in block:
                employment = "正社員"

            elif "有期雇用" in block:
                employment = "有期雇用"

            # 休日
            holiday_match = re.search(
                r"休日\s+(.+?)\s+求人番号",
                block,
                re.DOTALL
            )

            holiday = (
                holiday_match.group(1).strip()
                if holiday_match
                else ""
            )

            # 求人番号
            job_no_match = re.search(
                r"求人番号\s+(\d+\-\d+)",
                block
            )

            job_no = (
                job_no_match.group(1)
                if job_no_match
                else ""
            )

            # タグ
            tags = []

            tag_keywords = [
                "経験不問",
                "学歴不問",
                "資格不問",
                "転勤なし",
                "通勤手当あり",
                "マイカー通勤可",
                "オンライン自主応募可",
                "週休二日制（土日休）",
            ]

            for keyword in tag_keywords:

                if keyword in block:
                    tags.append(keyword)

            tags_text = " ".join(tags)

            # 仕事内容
            desc_match = re.search(
                r"仕事の内容\s+(.+?)\s+事業所名",
                block,
                re.DOTALL
            )

            description = (
                desc_match.group(1).strip()
                if desc_match
                else ""
            )

            # 空データ除外
            if title == "":
                continue

            job = {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "employment": employment,
                "holiday": holiday,
                "description": description,
                "tags": tags_text,
                "job_no": job_no,
            }

            job["score"] = calc_score(job)

            jobs.append(job)

        except Exception as e:

            print("解析失敗")
            print(e)

    # =========================
    # スコア順ソート
    # =========================

    jobs = sorted(
        jobs,
        key=lambda x: x["score"],
        reverse=True
    )

    # =========================
    # 表示
    # =========================

    print(f"\n取得件数: {len(jobs)}")

    print("\n===== 上位求人 =====\n")

    for i, job in enumerate(jobs[:10], start=1):

        print("=" * 60)

        print(f"順位: {i}")
        print(f"スコア: {job['score']}")
        print(f"職種: {job['title']}")
        print(f"会社: {job['company']}")
        print(f"勤務地: {job['location']}")
        print(f"給与: {job['salary']}")
        print(f"雇用形態: {job['employment']}")
        print(f"休日: {job['holiday']}")
        print(f"タグ: {job['tags']}")
        print(f"求人番号: {job['job_no']}")

        print("\n仕事内容:")
        print(job["description"][:300])

        print()

    browser.close()
