from fastapi import FastAPI
import uvicorn
from app import models
from app.database import engine
from app.routes import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5555)
