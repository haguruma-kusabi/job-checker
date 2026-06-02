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

    # =========================
    # GitHub Actions対応
    # =========================
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    page = browser.new_page()

    # =========================
    # 求人検索ページ
    # =========================
    print("求人検索ページ")

    page.goto(
        "https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?action=initDisp&screenId=GECA110010",
        wait_until="networkidle"
    )

    page.wait_for_timeout(3000)

    # =========================
    # 一般求人
    # =========================
    print("一般求人選択")

    try:
        page.get_by_role(
            "radio",
            name="一般求人"
        ).check(force=True)
    except Exception as e:
        print("一般求人選択失敗:", e)

    page.wait_for_timeout(1000)

    # =========================
    # 沖縄県選択
    # =========================
    print("沖縄県選択")

    page.locator(
        "#ID_todohukenHiddenAccoBtn"
    ).click(force=True)

    page.wait_for_timeout(3000)

    page.evaluate("""
        () => {

            const checkbox =
                document.querySelector(
                    '#ID_skCheck47947'
                );

            if (checkbox) {

                checkbox.checked = true;

                checkbox.dispatchEvent(
                    new Event(
                        'change',
                        { bubbles:true }
                    )
                );

                console.log("沖縄選択成功");
            }
        }
    """)

    page.wait_for_timeout(1000)

    # =========================
    # 都道府県決定
    # =========================
    print("都道府県決定")

    try:

        page.locator(
            "#ID_saveBtn"
        ).first.click(force=True)

    except:

        buttons = page.locator("button")

        for i in range(buttons.count()):

            txt = buttons.nth(i).inner_text()

            if "決定" in txt:

                buttons.nth(i).click(
                    force=True
                )

                break

    page.wait_for_timeout(3000)

    # =========================
    # 職種カテゴリ選択
    # =========================
    print("警備・ビル等の管理")

    page.evaluate("""
        () => {

            const checkbox =
                document.querySelector(
                    '#ID_daiEasyShokusyuBox5'
                );

            if (checkbox) {

                checkbox.checked = true;

                checkbox.dispatchEvent(
                    new Event(
                        'change',
                        { bubbles:true }
                    )
                );

                console.log("カテゴリ選択成功");
            }
        }
    """)

    page.wait_for_timeout(2000)

    # =========================
    # モーダルを開く
    # =========================
    print("職種モーダルを開く")

    buttons = page.locator(
        "input[value='決定']"
    )

    print(
        "決定ボタン数:",
        buttons.count()
    )

    for i in range(buttons.count()):

    try:

    print(
        i,
    buttons.nth(i).is_visible()
            )
    
    except:
    pass

    page.locator(
        "#ID_LdaiEasyShokusyuBox5"
    ).click(force=True)

    page.wait_for_timeout(2000)

    # =========================
    # 施設警備
    # =========================
    print("施設警備要素確認")

    print(
        page.locator(
            "#ID_easyShokusyuBox501"
        ).count()
    )

    print(
        page.locator(
        "#ID_modalTmpEasyShokusyuBox501"
        ).count()
    )
    print("管理人要素確認")

    print(
        page.locator(
            "#ID_easyShokusyuBox503"
        ).count()
    )

    print(
        page.locator(
            "#ID_modalTmpEasyShokusyuBox503"
        ).count()
    )

    print("施設警備選択")

    page.evaluate("""
        () => {

            const cb =
                document.querySelector(
                    '#ID_modalTmpEasyShokusyuBox501'
                ) ||
                document.querySelector(
                    '#ID_easyShokusyuBox501'
                );

            if (cb) {

                cb.checked = true;

                cb.dispatchEvent(
                    new Event(
                        'change',
                        { bubbles:true }
                    )
                );

                console.log("施設警備選択成功");
            }
        }
    """)

    # =========================
    # マンション・ビル等管理人
    # =========================
    print("マンション・ビル等管理人選択")

    page.evaluate("""
        () => {

            const cb =
                document.querySelector(
                    '#ID_modalTmpEasyShokusyuBox503'
                ) ||
                document.querySelector(
                    '#ID_easyShokusyuBox503'
                );

            if (cb) {

                cb.checked = true;

                cb.dispatchEvent(
                    new Event(
                        'change',
                        { bubbles:true }
                    )
                );

                console.log("マンション・ビル等管理人選択成功");
            }
        }
    """)

    page.wait_for_timeout(1000)

    # =========================
    # 選択状態確認
    # =========================
    print("職種選択状態確認")

    selected_jobs = page.evaluate("""
        () => {

            return [...document.querySelectorAll(
                'input[name="modalTmpEasyShokusyuBox"]:checked, input[name="easyShokusyuBox"]:checked'
            )].map(x => ({
                value:x.value,
                id:x.id
            }));
        }
    """)

    print(selected_jobs)

    # =========================
    # モーダル決定
    # =========================
    print("職種決定")

    try:

        page.locator(
            "input[value='決定']"
        ).first.click(force=True)

    except Exception as e:

        print("決定ボタン失敗:", e)

    page.wait_for_timeout(3000)

    # =========================
    # 検索条件確認
    # =========================
    print("===== 検索条件確認 =====")

    print("都道府県")
    print(
        page.locator(
            "#ID_todohukenHidden"
        ).input_value()
    )

    print("施設警備")
    print(
        page.locator(
            "#ID_easyShokusyuBox501"
        ).is_checked()
    )

    print("管理人")
    print(
        page.locator(
            "#ID_easyShokusyuBox503"
        ).is_checked()
    )

    # =========================
    # 検索前HTML保存
    # =========================
    with open(
        "before_search.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(page.content())

    page.screenshot(
        path="09_before_search.png"
    )

    print("検索前URL")
    print(page.url)

    # =========================
    # 検索
    # =========================

    # =========================
    # 結果取得
    # =========================
    print("検索結果URL")
    print(page.url)

    body_text = page.locator(
        "body"
    ).inner_text()

    with open(
        "result.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(page.content())

    with open(
        "body.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(body_text)

    print(body_text[:5000])

    # =========================
    # 求人抽出
    # =========================
    print("\n===== スコアリング =====\n")

    pattern = r"職種\s+(.*?)\s+職種解説"

    jobs = re.findall(
        pattern,
        body_text,
        re.S
    )

    if not jobs:

        print("求人抽出失敗")

    else:

        for i, job in enumerate(
            jobs[:20],
            start=1
        ):

            text = " ".join(
                job.split()
            )

            score = calculate_score(
                text
            )

            print(
                f"{i}. スコア:{score}"
            )

            print(text)

            print("-" * 80)

    browser.close()
