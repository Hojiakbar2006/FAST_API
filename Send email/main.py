from fastapi import FastAPI, BackgroundTasks, status

from app.config import MailBody
from app.mailer import send_mail

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Fast api is running"}


@app.post("/send-email")
def schedule_mail(req: MailBody, tasks: BackgroundTasks):
    data = req.dict()
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}