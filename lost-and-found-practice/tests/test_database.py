from app.database import DATABASE_PATH


def test_database_path_uses_project_root():
    assert DATABASE_PATH.name == "lost_and_found.db"
    assert DATABASE_PATH.parent.name == "lost-and-found-practice"
