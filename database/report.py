from .db import Base

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME

class Report(Base):
    __tablename__ = 'reports'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    report = Column(VARCHAR(32), nullable=False)
    created_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    @staticmethod
    def session_report(sess, user_id: int, report: str):
        return sess.add(
            Report(
                user_id=user_id,
                report=report
            )
        )
