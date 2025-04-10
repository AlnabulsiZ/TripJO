from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..APIs.account_info import get_user_from_token
from fastapi.security import OAuth2PasswordBearer
from ..models.serializers import getGuideInfo
from ..DB.tables import User 
from ..DB.database import get_db

rou = APIRouter()
auth_token = OAuth2PasswordBearer(tokenUrl="login")

@rou.post("/show_guide/", response_model= getGuideInfo)
def show_place(
    GuideInfo: getGuideInfo, 
    token: str = Depends(auth_token), 
    db: Session = Depends(get_db)
):
    user_id = get_user_from_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    guide = db.query(User).filter(
        User.id == GuideInfo.id,
        User.role == "guide"
    ).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    return guide

   