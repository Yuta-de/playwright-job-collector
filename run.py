from core.excel_io import read_keywords, export_projects
from core.scraper import operate_playwright

# 入出力設定
keyword_file_path = "input/search_info.xlsx"
output_file_path = "output/test.xlsx"

# 操作
keywords = read_keywords(keyword_file_path)
all_results = operate_playwright(keywords)
export_projects(all_results, output_file_path)