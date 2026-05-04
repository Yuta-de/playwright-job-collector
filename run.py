from core.excel_io import read_keywords, export_projects
from core.scraper import operate_playwright

from core.repository import init_db,insert_projects, get_projects

# 入出力設定
keyword_file_path = "input/search_info.xlsx"
output_file_path = "output/test.xlsx"

# 操作
keywords = read_keywords(keyword_file_path)
all_results = operate_playwright(keywords)

init_db()
insert_projects(all_results)

print("データベース:", get_projects())

export_projects(all_results, output_file_path)