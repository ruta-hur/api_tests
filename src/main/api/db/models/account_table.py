from sqlalchemy import Integer, Column, String, Float, ForeignKey
from src.main.api.db.base import base


class Account(base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey('user.id') , autoincrement = True)
    number = Column(String, unique = True, nullable = False)
    balance = Column(Float, nullable = False)

    def __repr__(self):
        return f"<Account(id={self.id}, user_id={self.user_id}, number={self.number}, balance={self.balance})>"