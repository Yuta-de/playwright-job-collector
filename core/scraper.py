from typing import Dict
from playwright.sync_api import sync_playwright

from core.normalizer import normalize_project

# 検索結果を返す関数
def fetch_projects(page, keyword:str) -> list[Dict]:
    results = []
    page.goto(("https://freelance-hub.jp/project/search/"))
    page.locator('input[type="search"]').fill(keyword)
    
    count_locator = page.locator('.ProjectListResult_CountTotal')
    old_count_text = count_locator.inner_text().strip()

    page.locator('//*[@class="SearchBar_FormNav"]/button').click()

    page.wait_for_function(
    """(oldText) => {
        const el = document.querySelector('.ProjectListResult_CountTotal');
        return el && el.textContent.trim() !== oldText;
    }""",
    arg=old_count_text
    )

    projects = page.locator('.ProjectCard')
    count = projects.count()
    # print(f"案件数：{count}")

    selectors = {
                "title":'.ProjectCard_Title',
                "tags":'.ProjectCard_Tags .TagLink',
                "money":'.ProjectCard_SummaryItem--money',
                "contract":'.ProjectCard_SummaryItem--contract',
                "location":'.ProjectCard_SummaryItem--location',
                "station":'.ProjectCard_SummaryItem--station',
                "skills":'.ProjectCard_SummaryItem--skill .TagLink',
                "occupations":'.ProjectCard_SummaryItem--occupation .TagLink',
                "update_date":'.ProjectCard__Footer__Info span:first-child',
                "publisher":'.ProjectCard__Footer__Info span:last-child'
    }

    for i in range(min(2, count)):
        project_card = projects.nth(i)
        raw_summary = {}
        # serch_info = {"keyword": keyword, "rank": i+1}
        serch_info = {"keyword": keyword}
        
        card_id = project_card.get_attribute("id")
        project_id = card_id.replace("ProjectListPc_ProjectCard_", "")
        print(f"{project_id=}")
        
        for key, val in selectors.items():
            # print(f"key:{key} , val:{val}")
            project_item = project_card.locator(val)
            if project_item.count() > 0:
                text_list = project_item.all_inner_texts()
            else:
                text_list = ["表記なし"]
            raw_summary[key] = text_list
        # print("summary:",raw_summary)
        raw_summary["project_id"] = [project_id]
        print(f"{raw_summary=}")
        summary = normalize_project(raw_summary)
        
        results.extend([serch_info | summary])
    return results

# playwrightを操作する関数
def operate_playwright(keywords:list,) -> list:
    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for keyword in keywords:
            results = fetch_projects(page, keyword)
            # print("result", results)
            all_results.extend(results)
        # print("all_results: ", all_results)
        browser.close()
    
    return all_results