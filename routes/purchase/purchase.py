from fastapi import APIRouter, Depends, Response
from database import *
from micro import auth_method, VerifyBody

router = APIRouter()

@router.post("/pay")
async def pay(amount: int, response: Response, token: VerifyBody = Depends(auth_method)):
    if not token.success:
        return token.payload

    if amount < 0:
        response.status_code = 400
        return {"message": "Invalid amount"}
    
    user_id = token.payload.id
    current_credit = Credit.update(user_id, amount, "유상 결제 렌즈 (충전)")
    return {"message": "success", "credit": current_credit}