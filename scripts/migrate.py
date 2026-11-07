"""Simple versioned SQLite migrations for educational demo.

Usage: python -m scripts.migrate [--db data/buildmart.db] [--target V001]
For a real shared PostgreSQL service use a dedicated migration tool, backups,
concurrency control, approvals, and deploy-time migration phase.
"""
import argparse
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path

MIGRATIONS = Path(__file__).resolve().parents[1] / 'database' / 'migrations'


def run_migrations(db_path: Path | str, target: str | None = None) -> list[str]:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    scripts = sorted(MIGRATIONS.glob('V[0-9]*__*.sql'))
    if target is not None and target not in {f.name.split('__')[0] for f in scripts}:
        raise ValueError(f'Unknown target migration: {target}')
    with closing(sqlite3.connect(db_path)) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        connection.commit()
        applied = {row[0] for row in connection.execute('SELECT version FROM schema_migrations')}
        completed = []
        for script in scripts:
            version = script.name.split('__')[0]
            if target is not None and version > target:
                break
            if version in applied:
                continue
            if not re.fullmatch(r'V\d+', version):
                raise ValueError('Unexpected migration version')
            sql = script.read_text(encoding='utf-8')
            # sqlite3.executescript does not automatically wrap in a transaction.
            safe_filename = script.name.replace("'", "''")
            connection.executescript(
                'BEGIN IMMEDIATE;\n' + sql +
                f"\nINSERT INTO schema_migrations(version, filename) VALUES ('{version}', '{safe_filename}');\n" +
                'COMMIT;'
            )
            completed.append(version)
        return completed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default=os.getenv('BUILDMART_DB_PATH', 'data/buildmart.db'))
    parser.add_argument('--target', default=None)
    args = parser.parse_args()
    versions = run_migrations(args.db, args.target)
    print('Applied:', ', '.join(versions) if versions else 'none (up to date)')


if __name__ == '__main__':
    main()
