from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
import jwt
import os
import secrets
from sqlalchemy.orm import Session
from ..DB.database import get_db
from werkzeug.security import check_password_hash
from fastapi.security import OAuth2PasswordBearer
from ..models.serializers import LoginRequest
from ..DB.tables import User

rou = APIRouter()


key = secrets.token_hex(32)
secret_key = os.getenv("SECRET_KEY", key)
algo = "HS256"
access_token_expire_time_minutes = 60

auth_token = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expire_delta: timedelta = timedelta(minutes=access_token_expire_time_minutes)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algo)

@rou.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
   
    dbUser = db.query(User).filter(User.Email == user.email).first() # => find user email

    if not dbUser:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not check_password_hash(dbUser.Password, user.password): # => check hashed password
        raise HTTPException(status_code=401, detail="Invalid email or password")

   
    token_data = { # => create access token
        "sub": dbUser.Email,
        "role": dbUser.Role
    }
    AccessToken = create_access_token(data=token_data)

    return {
        "access_token": AccessToken,
        "token_type": "bearer",
        "user_role": dbUser.Role
    }
