from core.excel_io import read_keywords, export_projects
from core.scraper import operate_playwright

from core.repository import init_db,insert_projects, get_projects, filter_new_projects

# 入出力設定
keyword_file_path = "input/search_info.xlsx"
output_file_path = "output/test.xlsx"

# 操作
keywords = read_keywords(keyword_file_path)
all_results = operate_playwright(keywords)

init_db()

insert_data = filter_new_projects(all_results)
# print("インサートデータ:", insert_data)

insert_projects(insert_data)

# print("データベース:", get_projects())


export_projects(insert_data, output_file_path)