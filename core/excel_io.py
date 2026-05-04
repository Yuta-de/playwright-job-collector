from pathlib import Path

import pandas as pd

from core.repository import PROJECT_COLUMNS

# キーワードを読み込む関数
def read_keywords(file_path:str) -> list:
    keyword_file_path = Path(file_path)
    search_info_df = pd.read_excel(keyword_file_path, sheet_name="search_info")
    search_keywords = search_info_df["keyword"].to_list()
    return search_keywords

# Excel出力する関数
def export_projects(all_results:list, file_path:str) -> None:
    output_path = Path(file_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl", ) as writer:
        df = pd.DataFrame(all_results) #keywordごと
        # print("df:",df)
        column_name = PROJECT_COLUMNS
        df.to_excel(writer, sheet_name="案件一覧", index=False, columns=column_name)
