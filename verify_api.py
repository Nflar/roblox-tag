# ================= FASTAPI SETUP =================
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime, timedelta
import asyncio

app = FastAPI()

verification_codes = {}  # discord_user_id -> {code, expires}

class VerifyRequest(BaseModel):
    username: str
    code: int

@app.post("/verify")
def verify(req: VerifyRequest, background_tasks: BackgroundTasks):
    user_id = None
    # Find the code
    for uid, entry in verification_codes.items():
        if entry["code"] == req.code:
            if datetime.utcnow() > entry["expires"]:
                del verification_codes[uid]
                raise HTTPException(status_code=400, detail="Code expired")
            user_id = uid
            break
    if not user_id:
        raise HTTPException(status_code=404, detail="Invalid code")

    # Delete used code
    del verification_codes[user_id]

    # Schedule role assignment in bot's loop
    if bot.is_ready():  # make sure bot is running
        loop = asyncio.get_event_loop()
        loop.create_task(assign_verified_role(user_id))

    return {"discord_id": user_id, "username": req.username, "verified": True}
