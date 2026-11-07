from pathlib import Path
import pytest
from scripts.migrate import run_migrations


@pytest.fixture
def migrated_db(tmp_path: Path) -> Path:
    db_path = tmp_path / 'buildmart.db'
    run_migrations(db_path)
    return db_path
