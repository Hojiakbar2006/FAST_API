from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def read_all():
    return {"message": "success"}
