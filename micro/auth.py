from dataclasses import dataclass
import traceback
from fastapi import Query
from fastapi.responses import Response, JSONResponse
import requests

from env import MicroEnv


@dataclass
class TokenPayload:
    id: int

@dataclass
class VerifyBody:
    success: bool
    payload: TokenPayload | str | Response

async def auth_method(token: str = Query(...)) -> VerifyBody:
    def error(code, msg):
        return VerifyBody(success=False, payload=JSONResponse(status_code=code, content={'error': msg} if msg else None))

    if not token.strip():
        return error(400, 'Invalid token')
    
    try:
        res = Auth.verify(token)

        if not res.success:
            return error(401, res.payload)
        
        res.payload = TokenPayload(**res.payload)

        return res
    except KeyError: return VerifyBody(success=False, payload=Response(status_code=401))
    except: 
        traceback.print_exc()
        return error(500, 'micro service error')


class Auth:
    @staticmethod
    def verify(token: str, check_active: bool=True) -> VerifyBody:
        res = requests.get(
            f'http://{MicroEnv.AUTH}/internal/auth/verify',
            params={
                'token': token,
                'check_active': check_active
            }
        )

        if res.status_code != 200:
            raise Exception(res.status_code)
        
        return VerifyBody(**res.json())
