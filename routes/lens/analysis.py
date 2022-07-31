import traceback
import cv2
import numpy as np
from fastapi import Response, Depends, UploadFile, File
from fastapi.routing import APIRouter
from core.predict import Predict
from micro import auth_method, VerifyBody

router = APIRouter(prefix='/analysis')

@router.post('/')
async def predict(
    res: Response,
    token: VerifyBody = Depends(auth_method),
    image: UploadFile = File(...)
):
    def error(code: int, msg: str):
        res.status_code = code
        return {'error': msg}

    if not token.success:
        return token.payload

    try:
        img = cv2.imdecode(np.frombuffer(await image.read(), np.uint8), cv2.IMREAD_COLOR)
        h, w, c = img.shape

        if c != 3 or h < 416 or w < 416 or h > 2560 or w > 2560:
            return error(400, 'image format error')
    except:
        return error(400, 'image format error')
    
    try:
       report = Predict.analysis(img)
    except:
        traceback.print_exc()
        return error(500, 'analysis service error')
    
    return {
        'report': report
    }
    