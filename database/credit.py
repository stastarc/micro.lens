# 없애면 안돼ㅑ요~
from .db import engine, factory, scope

from sqlalchemy import Column, DateTime, func, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, VARCHAR
from .db import Base

class Credit(Base):
    __tablename__ = 'credits'

    user_id = Column(BIGINT)
    credit = Column(INTEGER)
    comment = Column(VARCHAR(100))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    @staticmethod
    def update(sess, user_id: int, credit: int, comment: str) -> int | None:
        return sess.query(func.update_credit(user_id, credit, comment[:70]))
