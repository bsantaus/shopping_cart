from sqlmodel import create_engine, SQLModel
from config import settings

db = None

class DB:
    def __init__(self):
        conn_str = (
            "postgresql://{user}:{password}@{host}:{port}/{database}"
            .format(
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
            )
        )
        self._engine = create_engine(conn_str)
        SQLModel.metadata.create_all(self._engine)

def sc_database():
    global db
    if not db:
        db = DB()
    return db