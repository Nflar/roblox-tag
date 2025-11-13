from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

# Allow Roblox and Discord bot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verification_codes = {}  # discord_id -> {code, expires}

@app.get("/")
def root():
    return {"status": "OK", "message": "Verification API running!"}

# Called by Discord bot when user gets a code
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
    print(f"[REGISTER] Code {req.code} for {req.discord_id}")
    return {"success": True}

# Called by Roblox when player submits code
class VerifyRequest(BaseModel):
    username: str
    userId: int
    code: int

@app.post("/verify")
def verify(req: VerifyRequest):
    for discord_id, entry in list(verification_codes.items()):
        if entry["code"] == req.code:
            if datetime.utcnow() > entry["expires"]:
                del verification_codes[discord_id]
                raise HTTPException(status_code=400, detail="Code expired")

            del verification_codes[discord_id]
            print(f"[VERIFY] {req.username} verified as {discord_id}")
            return {"verified": True, "discord_id": discord_id}

    raise HTTPException(status_code=404, detail="Invalid code")
