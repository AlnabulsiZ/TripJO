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

    place = db.query(Place).filter(Place.OwnerId == user_id, Place.Name == place_info.name, Place.City == place_info.city).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    images = db.query(Image).filter(Image.PlaceId == place.Id).all()
    image_list = [getImage(image_path=image.ImagePath) for image in images]

    is_fav = db.query(Favorites).filter(Favorites.UserId == user_id, Favorites.PlaceId == place.Id).first() is not None

    comments = db.query(Comment).filter(Comment.PlaceId == place.Id).all()

    return {
        "Id": place.Id,
        "Name": place.Name,
        "City": place.City,
        "Type": place.Type,
        "Description": place.Description,
        "Rate": place.Rate,
        "Images": image_list,
        "IsINFav": is_fav,
        "Comments": [comment.Comment for comment in comments]  
        }
