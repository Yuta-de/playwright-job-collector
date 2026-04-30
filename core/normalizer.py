from typing import Dict
from datetime import datetime, timedelta

## 整形する関数
def normalize_project(raw_project: Dict) -> Dict:

    project = {}

    for key, val in raw_project.items():
        if key in ["tags","skills","occupations"]:
            project[key] = [new_val.strip() for new_val in val]
        else:
            new_val = val[0]
            if key == "update_date":
                date_text = new_val.replace("・","").strip()
                project[key] = parse_update_date(date_text)
            elif key == "publisher":
                project[key] = new_val.replace("提供元:","").strip()
            elif key == "money":
                project[key] = new_val.replace(u"\xa0",u"").strip()
            else:
                project[key] = new_val.strip()
    
    # print("project:", project)
    return project


# 日付の表示を変換する関数
def parse_update_date(date_text: str) -> str:
    now = datetime.now()
    if date_text == "今日":
        new_val = now.strftime('%Y-%m-%d')
    elif "日前" in date_text:
        days = int(date_text.replace("日前",""))
        new_val = (now - timedelta(days=days)).strftime('%Y-%m-%d')
    elif "ヶ月前" in date_text:
        days = int(date_text.replace("ヶ月前","")) * 30
        new_val = (now - timedelta(days=days)).strftime('%Y-%m-%d')
    else:
        new_val = f"日付変換不可:{date_text}"
    return new_val
