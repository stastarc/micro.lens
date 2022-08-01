from .db import Base

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, LONGTEXT, DATETIME

NAMES = [
    'ko',
    'en',
    'jp',
    'zh',
]

class Plant(Base):
    __tablename__ = 'plants'

    id = Column(BIGINT, primary_key=True)
    tags = Column(VARCHAR(500), nullable=False)
    names = Column(VARCHAR(200), nullable=False)
    short_description = Column(VARCHAR(100), nullable=False)
    description = Column(VARCHAR(2000), nullable=False)
    images = Column(VARCHAR(320), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    relevant_plants = Column(VARCHAR(100), nullable=False)
    updated_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    @staticmethod
    def parse_names(names: str) -> dict[str, str]:
        names = names.split(',')
        return {NAMES[i]: v for i, v in enumerate(names)}

    @staticmethod
    def parse_images(images: str) -> list[str]:
        return images.split(',')
    
    @staticmethod
    def parse_relevant_plants(relevant_plants: str) -> list[str]:
        return relevant_plants.split(',')