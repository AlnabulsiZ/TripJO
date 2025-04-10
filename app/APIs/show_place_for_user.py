from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..APIs.account_info import get_user_from_token
from fastapi.security import OAuth2PasswordBearer
from ..models.serializers import getPlaceInfo, getImage
from ..DB.tables import Place, Image, Favorites, Comment 
from ..DB.database import get_db

rou = APIRouter()
auth_token = OAuth2PasswordBearer(tokenUrl="login")


@rou.post("/show_place/")
def show_place(place_info: getPlaceInfo, token: str = Depends(auth_token), db: Session = Depends(get_db)):
    user_id = get_user_from_token(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    place = db.query(Place).filter(Place.owner_id == user_id, Place.name == place_info.name, Place.city == place_info.city).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    images = db.query(Image).filter(Image.place_id == place.id).all()
    image_list = [getImage(image_path=image.image_path) for image in images]

    is_fav = db.query(Favorites).filter(Favorites.user_id == user_id, Favorites.place_id == place.id).first() is not None

    comments = db.query(Comment).filter(Comment.place_id == place.id).all()

    return {
        "Id": place.id,
        "Name": place.name,
        "City": place.city,
        "Type": place.type,
        "Description": place.description,
        "Rate": place.rate,
        "Images": image_list,
        "IsINFav": is_fav,
        "Comments": [Comment.comment for comment in comments]  
        }
