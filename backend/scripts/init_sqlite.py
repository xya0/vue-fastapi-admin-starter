"""创建并初始化 SQLite 测试数据库。"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "youlai_admin_test.db"
SQL_PATH = ROOT / "sql" / "sqlite" / "youlai-admin.sql"


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
