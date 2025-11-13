from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

app = FastAPI()

# Store verification codes: discord_user_id -> {code, expires}
verification_codes = {}

class VerifyRequest(BaseModel):
    username: str
    code: int

@app.post("/verify")
def verify(req: VerifyRequest):
    user_id = None
    # Find code
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

    return {"discord_id": user_id, "username": req.username, "verified": True}

@app.get("/")
def root():
    return {"status": "FastAPI running!"}
