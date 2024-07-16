from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

URL_DATABASE = "mysql+pymysql://root:123456@localhost:3306/todos"
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

'''
with engine.connect() as connection:
    connection.execute(text('ALTER TABLE todos ADD COLUMN description INTEGER DEFAULT 0'))
'''

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
