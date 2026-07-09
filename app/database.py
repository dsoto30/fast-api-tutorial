from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


sync_engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autoflush=False, bind=sync_engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn_string = conninfo.make_conninfo(dbname="fastapi", port=5432, user="postgres", password="strike30", connect_timeout=10)
#         conn = psycopg.connect(conninfo=conn_string, row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as err:
#         print(f"Connecting to database failed")
#         print("Error", err)
#         time.sleep(2)