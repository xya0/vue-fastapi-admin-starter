"""创建并初始化 SQLite 测试数据库。"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = next((ROOT / "data").iterdir(), None)  # DB_PATH = ROOT / "data" / "app.db"
SQL_PATH = next((ROOT / "sql" / "sqlite").iterdir(), None)  # SQL_PATH = ROOT / "sql" / "sqlite" / "admin.sql"

# 确保文件确实存在
if not DB_PATH or not DB_PATH.is_file():
    raise FileNotFoundError(f"在目录下未找到任何数据库文件。")

if not SQL_PATH or not SQL_PATH.is_file():
    raise FileNotFoundError(f"在目录下未找到任何 SQL 脚本文件。")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQL_PATH.read_text(encoding="utf-8"))

    print(f"SQLite database initialized: {DB_PATH}")


if __name__ == "__main__":
    main()
