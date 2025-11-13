from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store codes: roblox_userid -> {username, code, expires}
roblox_codes = {}
# Store linked users: discord_id -> roblox_name
linked_users = {}

@app.get("/")
def root():
    return {"status": "OK", "message": "Verification API active"}

# From Roblox server
class RobloxRegister(BaseModel):
    userId: int
    username: str
    code: int

@app.post("/register")
def register(req: RobloxRegister):
    roblox_codes[req.userId] = {
        "username": req.username,
        "code": req.code,
        "expires": datetime.utcnow() + timedelta(minutes=10)
    }
    print(f"[REGISTER] {req.username} ({req.userId}) -> {req.code}")
    return {"success": True}

# From Discord bot
class DiscordVerify(BaseModel):
    discord_id: str
    code: int

@app.post("/verify")
def verify(req: DiscordVerify):
    for uid, data in list(roblox_codes.items()):
        if data["code"] == req.code:
            if datetime.utcnow() > data["expires"]:
                del roblox_codes[uid]
                raise HTTPException(status_code=400, detail="Code expired")

            del roblox_codes[uid]
            linked_users[req.discord_id] = data["username"]
            print(f"[LINKED] Discord {req.discord_id} ↔ Roblox {data['username']}")
            return {"verified": True, "roblox_name": data["username"]}

    raise HTTPException(status_code=404, detail="Invalid code")
