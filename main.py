import threading
from fastapi import FastAPI
from core.predict import Predict
from env import Env
import routes, middleware

app = FastAPI()

middleware.include(app)
routes.include(app)

@app.on_event('startup')
async def startup():
    threading.Thread(target=Predict.init())

@app.on_event('shutdown')
async def shutdown():
    Predict.dispose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=Env.HOST,
        port=Env.PORT,
        reload=False,
        log_config="./logging.ini" if not Env.DEBUG else None
    )