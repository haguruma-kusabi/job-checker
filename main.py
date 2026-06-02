from playwright.sync_api import sync_playwright
import re

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

    # =========================
    # トップページ
    # =========================
    print("トップページアクセス")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/",
        wait_until="networkidle"
    )

    page.screenshot(path="01_top_page.png")

    # =========================
    # 求人検索
    # =========================
    print("求人情報検索クリック")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?action=initDisp&screenId=GECA110010",
        wait_until="networkidle"
    )

    page.screenshot(path="02_search_page.png")

    # =========================
    # 一般求人
    # =========================
    print("一般求人チェック")

    page.wait_for_timeout(3000)

    ippan = page.get_by_role("radio", name="一般求人")

    if ippan.count() > 0:
        ippan.first.check(force=True)

    page.screenshot(path="03_after_ippan.png")

    # =========================
    # 就業場所
    # =========================
    print("就業場所選択")

    page.locator("#ID_todohukenHiddenAccoBtn").click(force=True)

    page.wait_for_timeout(3000)

    page.screenshot(path="04_prefecture_modal.png")

    # =========================
    # 沖縄選択
    # =========================
    print("沖縄選択")

    page.evaluate("""
        () => {
            const checkbox = document.querySelector('#ID_skCheck47947');
            if (checkbox) {
                checkbox.checked = true;
                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    """)

    page.wait_for_timeout(1000)

    page.screenshot(path="05_okinawa_selected.png")

    # =========================
    # 決定
    # =========================
    print("都道府県決定")

    buttons = page.locator("button")

    for i in range(buttons.count()):
        text = buttons.nth(i).inner_text()

        if "決定" in text:
            buttons.nth(i).click(force=True)
            break

    page.wait_for_timeout(3000)

    page.screenshot(path="06_after_prefecture_confirm.png")

    # =========================
    # 職種カテゴリ
    # =========================
    print("職種カテゴリ選択")

    page.screenshot(path="07_before_jobtype.png")

    page.evaluate("""
        () => {

            const labels = [...document.querySelectorAll("label")];

            for (const label of labels) {

                if (label.innerText.includes("警備・ビル等の管理")) {

                    const id = label.getAttribute("for");

                    const checkbox = document.getElementById(id);

                    if (checkbox) {

                        checkbox.checked = true;

                        checkbox.dispatchEvent(
                            new Event('change', { bubbles:true })
                        );

                        console.log("選択成功", id);
                    }
                }
            }
        }
    """)

    page.wait_for_timeout(2000)

    page.screenshot(path="08_after_jobtype.png")

    # =========================
    # 検索前確認
    # =========================
    print("検索実行前")

    page.screenshot(path="09_before_search.png")

    print("検索前URL")
    print(page.url)

    # =========================
    # 検索実行
    # =========================
    print("検索実行")

    page.locator("#ID_searchBtn").click(force=True)

    page.wait_for_timeout(5000)

    page.screenshot(path="10_after_search.png")

    # =========================
    # 結果表示
    # =========================
    print("\n現在URL:\n")
    print(page.url)

    print("\nタイトル:\n")
    print(page.title())

    body_text = page.locator("body").inner_text()

    print("\n===== 検索結果先頭 =====\n")
    print(body_text[:5000])

    # HTMLも保存
    with open("result.html", "w", encoding="utf-8") as f:
        f.write(page.content())

    # BODY全文も保存
    with open("body.txt", "w", encoding="utf-8") as f:
        f.write(body_text)

    # =========================
    # 求人抽出
    # =========================
    print("\n===== スコアリング =====\n")

    pattern = r"職種\s+(.*?)\s+職種解説"

    jobs = re.findall(pattern, body_text, re.S)

    if len(jobs) == 0:
        print("求人が取得できませんでした")
    else:
        for i, job in enumerate(jobs[:10], start=1):

            clean_job = " ".join(job.split())

            score = calculate_score(clean_job)

            print(f"{i}. スコア:{score}")
            print(clean_job)
            print("-" * 50)

    browser.close()
