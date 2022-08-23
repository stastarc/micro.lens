from .db import Base

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, LONGTEXT, DATETIME

NAMES = [
    'ko',
    'en',
    'ja',
    'zh',
]

class Plant(Base):
    __tablename__ = 'plants'

    id = Column(BIGINT, primary_key=True)
    tags = Column(VARCHAR(500), nullable=False)
    names = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(100), nullable=False)
    more_description = Column(VARCHAR(2000), nullable=False)
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
        count = len(images) // 32
        return [images[i*32:(i+1)*32] for i in range(count)]
    
    @staticmethod
    def parse_relevant_plants(relevant_plants: str) -> list[str]:
        return relevant_plants.split(',')