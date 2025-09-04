from fastapi import Depends, HTTPException, Header
from .models import UserOut
import jwt, os, time

SECRET = os.getenv("SECRET_KEY", "dev-secret")

def create_demo_user() -> UserOut:
    payload = {"sub": "demo-user", "email": "demo@example.com", "exp": int(time.time())+3600}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return UserOut(id="demo-user", email="demo@example.com", token=token)

def get_current_user(authorization: str | None = Header(default=None)) -> UserOut:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split()[1]
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return UserOut(id=data["sub"], email=data["email"], token=token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
