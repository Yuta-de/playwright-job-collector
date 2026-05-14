# DBを扱う

from pathlib import Path
import sqlite3

from typing import Dict, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "projects.db"

PROJECT_COLUMNS = ["keyword", "title", "tags", "money", "contract", "location", "station", "skills", "occupations", "update_date", "publisher", "project_id"]

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            title TEXT NOT NULL,
            tags TEXT NOT NULL,
            money TEXT NOT NULL,
            contract TEXT NOT NULL,
            location TEXT NOT NULL,
            station TEXT NOT NULL,
            skills TEXT NOT NULL,
            occupations TEXT NOT NULL,
            update_date TEXT NOT NULL,
            publisher TEXT NOT NULL,
            project_id TEXT NOT NULL UNIQUE
        )
        """)

        conn.commit()

def to_project_row(project:Dict) -> Tuple:
    row = []
    for column in PROJECT_COLUMNS:
        value = project[column]
        if column in ["tags", "skills", "occupations"]:
            value = ",".join(value)
        row.append(value)
    # print(f"project:{project}")
    tuple_project = tuple(row)
    # print(f"tuple_project: {tuple_project}")
    return tuple_project

def filter_new_projects(projects:list[Dict]) -> list[Dict]:
    existing_keys = get_key_from_projects()
    print(f"{existing_keys=}")
    new_projects = []

    for project in projects:
        key = project["project_id"]
        if key not in existing_keys:
            new_projects.append(project)
    
    return new_projects

def insert_projects(projects:list[Dict]) -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        insert_rows = [to_project_row(project) for project in projects]
        print(f"{insert_rows=}")

        query = f"""
                INSERT OR IGNORE
                INTO projects (
                  {','.join(PROJECT_COLUMNS)}
                )
                VALUES ({','.join(['?'] * len(PROJECT_COLUMNS))})
                """
        
        cursor.executemany(query, insert_rows)

def get_projects():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()
    return rows

def get_key_from_projects() -> set[str]:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT project_id FROM projects")
        rows = cursor.fetchall()
    return set(row[0] for row in rows)