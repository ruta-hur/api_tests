from sqlalchemy import Integer, Column, String, Float, ForeignKey, DateTime
from src.main.api.db.base import base


class Transaction(base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key = True, autoincrement = True)
    to_account_id = Column(Integer, nullable = False)
    from_account_id = Column(Integer, ForeignKey('account.id'), nullable = False)
    credit_id = Column(Integer, ForeignKey('credit.id'), nullable = False, unique = True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable = False)
    created_at = Column(DateTime, nullable=False)


    def __repr__(self):
        return f"<Transaction(id={self.id}, to_aacount_id={self.to_account_id}, from_aacount_id={self.from_account_id}, credit_id={self.credit_id}, amount={self.amount})>"