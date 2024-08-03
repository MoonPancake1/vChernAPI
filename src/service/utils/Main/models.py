from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey

from src.service.utils.db import Base


class Projects(Base):
    """
    Модель для проектов
    """

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    realize_project = Column(Date)
    stack = Column(JSON)
    status = Column(String)
    view = Column(Integer)
    link_logo = Column(String)
    github_link = Column(String)
    project_link = Column(String)


class Project_Grades(Base):
    """
    Модель для оценок проекта
    """

    __tablename__ = 'project_grades'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_uuid = Column(Integer, ForeignKey('users.uuid'))
    grade = Column(Integer)


class Project_Commetaries(Base):
    """
    Модель для комментариев к проекту
    """

    __tablename__ = 'project_commetaries'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_uuid = Column(Integer, ForeignKey('users.uuid'))
    comment = Column(String)