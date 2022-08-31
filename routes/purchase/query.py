from fastapi import APIRouter, Depends, Response
from database import *
from micro import auth_method, VerifyBody

router = APIRouter()

@router.post("/credits")
async def pay(response: Response, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload
    
    user_id = token.payload.id
    current_credit = Credit.update(user_id, 0, None)
    return {"message": "success", "credit": current_credit}