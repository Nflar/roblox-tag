from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

# Enable CORS for Roblox
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verification_codes = {}  # discord_id -> {code, expires}

# Root route (test)
@app.get("/")
def root():
    return {"status": "OK", "message": "Verification API running!"}

# Register a new code (called by bot)
class RegisterRequest(BaseModel):
    discord_id: str
    code: int
    expires: int

@app.post("/register")
def register(req: RegisterRequest):
    verification_codes[req.discord_id] = {
        "code": req.code,
        "expires": datetime.utcnow() + timedelta(seconds=req.expires)
    }
    return {"success": True, "message": "Code registered."}

# Roblox verify route
class VerifyRequest(BaseModel):
    username: str
    code: int

@app.post("/verify")
def verify(req: VerifyRequest):
    user_id = None

    for uid, entry in verification_codes.items():
        if entry["code"] == req.code:
            if datetime.utcnow() > entry["expires"]:
                del verification_codes[uid]
                raise HTTPException(status_code=400, detail="Code expired")
            user_id = uid
            break

    if not user_id:
        raise HTTPException(status_code=404, detail="Invalid code")

    del verification_codes[user_id]
    return {"discord_id": user_id, "username": req.username, "verified": True}
