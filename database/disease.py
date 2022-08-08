from __future__ import annotations

from dataclasses import dataclass
from .db import Base

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME

@dataclass
class DetailDiseaseData:
    id: int
    plant_id: int
    name: str
    images: list[str]
    content: str
    more_content: str
    updated_at: str

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(BIGINT, primary_key=True)
    plant_id = Column(BIGINT, nullable=False)
    code = Column(VARCHAR(80), nullable=False)
    plant_code = Column(VARCHAR(80), nullable=False)
    tags = Column(VARCHAR(500), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    images = Column(VARCHAR(128), nullable=False)
    content = Column(VARCHAR(300), nullable=False)
    more_content = Column(VARCHAR(1000), nullable=False)
    updated_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    @staticmethod
    def session_get(sess, plant_code: str, disease_code: str) -> Disease | None:
        return sess.query(Disease).filter(
            Disease.plant_code == plant_code,
            Disease.code == disease_code
        ).first()

    @staticmethod
    def get_detail(disease: 'Disease') -> DetailDiseaseData:
        return DetailDiseaseData(
            id=disease.id,
            plant_id=disease.plant_id,
            name=disease.name,
            images=Disease.parse_images(disease.images),
            content=disease.content,
            more_content=disease.more_content,
            updated_at=disease.updated_at
        )
    
    @staticmethod
    def session_get_detail(sess, plant_code: str, disease_code: str) -> DetailDiseaseData | None:
        disease = Disease.session_get(sess, plant_code, disease_code)
        
        if disease == None:
            return None

        return Disease.get_detail(disease)

    @staticmethod
    def parse_images(images: str) -> list[str]:
        count = len(images) // 32
        return [images[i*32:(i+1)*32] for i in range(count)]
    