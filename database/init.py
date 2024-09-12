from database.config import DatabaseConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.config import database_logger

# Движок SQLAlchemy создаётся на основе Postgres и драйвера psycopg2
print('DatabaseConfig.DB_USER, DatabaseConfig.DB_PASS, DatabaseConfig.DB_HOST, DatabaseConfig.DB_PORT, DatabaseConfig.DB_NAME')
print(DatabaseConfig.DB_USER, DatabaseConfig.DB_PASS, DatabaseConfig.DB_HOST, DatabaseConfig.DB_PORT, DatabaseConfig.DB_NAME)

database_logger.info(f"Creating engine: {DatabaseConfig.DB_USER}, {DatabaseConfig.DB_PASS}, {DatabaseConfig.DB_HOST}, {DatabaseConfig.DB_PORT}, {DatabaseConfig.DB_NAME}")

engine = create_engine(
    f"postgresql+psycopg2://{DatabaseConfig.DB_USER}:{DatabaseConfig.DB_PASS}@{DatabaseConfig.DB_HOST}:{DatabaseConfig.DB_PORT}/{DatabaseConfig.DB_NAME}"
)

def get_db():
    session_maker: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_maker()
    yield session
    session.close()
    