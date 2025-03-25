import sqlalchemy
from sqlalchemy import orm
from datetime import datetime
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = orm.relationship('User')