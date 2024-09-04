from datetime import datetime

from sqlalchemy import create_engine, TIMESTAMP, func
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr,
)

from src.config.config import settings, database

SQLALCHEMY_DATABASE_URL = (
    f"{settings.DB_ENGINE}://{database.POSTGRES_USER}:{database.POSTGRES_PASSWORD}@"
    + f"{settings.DB_HOST}/{database.POSTGRES_DB}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Базавая модель для всех моделей в проекте
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


# Dependency
def get_db():
    """
    Функция для создания сессии с базой данных
    :return: активная сессия с базойй данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
