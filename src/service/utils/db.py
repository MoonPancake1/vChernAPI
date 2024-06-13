from datetime import datetime

from sqlalchemy import create_engine, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, declared_attr

from src.config.project_config.config import settings
from src.service.utils import models


if settings.DEBUG:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./vChernTestDB.db"
else:
    SQLALCHEMY_DATABASE_URL = f"{settings.DB_ENGINE}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/" + \
                              f"{settings.DB_NAME}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/postgres"
# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:1@vchern.me:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Базавая модель для всех моделей в проекте
    """
    __abstarct__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now()
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


def initialize_database():
    """
    Функция для создания всех моделей в базе данных
    :return: None
    """
    models.Base.metadata.create_all(bind=engine)
