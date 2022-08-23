from typing import Literal
import requests
from env import MicroEnv

def search_market(query: str, mode: Literal['full', 'tag', 'name']) -> list[dict]:
    res = requests.get(
        f'http://{MicroEnv.MARKET}/internal/search',
        params={
            'query': query,
            'mode': mode
        }
    )

    if res.status_code != 200:
        return []

    return res.json()