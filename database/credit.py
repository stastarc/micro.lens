# 없애면 안돼ㅑ요~
from .db import engine, factory, scope

from sqlalchemy import Column, DateTime, func, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from .db import Base

class Credit(Base):
    __tablename__ = 'credits'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT)
    credit = Column(INTEGER)
    comment = Column(VARCHAR(100))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    @staticmethod
    def session_update(sess, user_id: int, credit: int, comment: str | None) -> int:
        return sess.query(func.update_credit(user_id, credit, comment[:70] if comment else None)).scalar()
    
    @staticmethod
    def update(user_id: int, credit: int, comment: str | None) -> int:
        with scope() as sess:
            return Credit.session_update(sess, user_id, credit, comment)
