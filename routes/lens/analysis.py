import traceback
import cv2
import numpy as np
from fastapi import Response, Depends, UploadFile, File
from fastapi.routing import APIRouter
from core.predict import Predict
from database import scope, Plants, Credit, Report
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
    
    user_id = token.payload.id
    c = Credit.update(user_id, 0, None)

    if c <= 0:
        return error(403, 'Lack of credit.')

    try:
        img = cv2.imdecode(np.frombuffer(await image.read(), np.uint8), cv2.IMREAD_COLOR)
        h, w, c = img.shape

        if c != 3 or h < 416 or w < 416 or h > 2560 or w > 2560:
            return error(400, 'image format error')
    except:
        return error(400, 'image format error')
    
    try:
       report = Predict.analysis(
            img,
            dump=True,
            des=f'user:{user_id}'
        )
    except:
        traceback.print_exc()
        return error(500, 'analysis service error')
    
    # 으으 이 불길한거
    del img
    
    if report != None:
        report, report_file = report
        with scope() as sess:
            # 우리먼저
            Report.session_report(sess, user_id, report_file)

            plant = Plants.session_search_detail(sess, report.name, 'name')

            if plant:
                plant.updated_at = plant.updated_at.isoformat()

            if Credit.session_update(sess, user_id, -1, f'analysis user:{user_id}') == -1: # 결과는 절대 안주지 ㅋㅋ
                return error(500, 'credit service error')
            
    else:
        plant = None
    
    return {
        'info': {
            'report': report,
            'plant': plant
        }
    }
    