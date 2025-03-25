import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    _tablename_ = 'departments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    chief = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    members = sqlalchemy.Column(sqlalchemy.ARRAY , nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship('User')