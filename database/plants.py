import json
from .plant import Plant

from typing import Literal
from datetime import datetime
from dataclasses import dataclass

PAGE_SIZE = 20

@dataclass
class ShortPlantData:
    id: int
    names: dict[str, str]
    image: str

@dataclass
class DetailPlantData:
    id: int
    names: dict[str, str]
    images: list[str]
    description: str
    more_description: str
    content: str
    relevent_plants: list[ShortPlantData]
    updated_at: datetime

class Plants:
    @staticmethod
    def fulltext_search_against(mode: Literal['full', 'name']) -> str:
        return f'MATCH (`names`{",`tags`,`short_description`" if mode=="full" else ""}) AGAINST (:q IN BOOLEAN MODE)'

    @staticmethod
    def session_search(sess, query: str, mode: Literal['full', 'name'], offset: int = 0, limit: int = PAGE_SIZE) -> list[Plant]:
        fulltext = Plants.fulltext_search_against(mode)
        return sess.execute(
            f'SELECT *, {fulltext} as score FROM `{Plant.__tablename__}` WHERE {fulltext} ORDER BY score DESC LIMIT {offset*PAGE_SIZE},{limit}',
            {'q': query}).all()
        
    @staticmethod
    def session_search_one(sess, query: str, mode: Literal['full', 'name']) -> Plant | None:
        fulltext = Plants.fulltext_search_against(mode)
        return sess.execute(f'SELECT *, {fulltext} as score FROM `{Plant.__tablename__}` WHERE {fulltext} LIMIT 1',
            {'q': query}).first()

    @staticmethod
    def session_search_short(sess, query: str, mode: Literal['full', 'name'], offset: int = 0) -> list[ShortPlantData]:
        return [Plants.get_short(p) for p in Plants.session_search(sess, query, mode, offset)]
    
    @staticmethod
    def session_search_short_one(sess, query: str, mode: Literal['full', 'name']) -> ShortPlantData | None:
        p = Plants.session_search_one(sess, query, mode)
        return Plants.get_short(p) if p else None

    @staticmethod
    def get_short(plant: Plant) -> ShortPlantData:
        return ShortPlantData(
            id=plant.id,
            names=Plant.parse_names(plant.names),
            image=next(iter(Plant.parse_images(plant.images)), ''),
        )
    
    @staticmethod
    def get_detail(sess, plant: Plant) -> DetailPlantData:
        return DetailPlantData(
            id=plant.id,
            names=Plant.parse_names(plant.names),
            images=Plant.parse_images(plant.images),
            description=plant.description,
            more_description=plant.more_description,
            content=json.loads(plant.content),
            relevent_plants=[p for p in
                                [Plants.session_search_short_one(sess, plant, 'name')
                                    for plant in Plant.parse_relevant_plants(plant.relevant_plants)]
                                if p != None],
            updated_at=plant.updated_at,
        )
    
    @staticmethod
    def session_search_detail(sess, query: str, mode: Literal['full', 'name']) -> DetailPlantData | None:
        p = Plants.session_search_one(sess, query, mode)
        return Plants.get_detail(sess, p) if p else None