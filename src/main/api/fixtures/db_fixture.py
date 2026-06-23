import pytest
from src.main.api.db.engine import sessionLocal, engine


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionLocal(bind = connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()