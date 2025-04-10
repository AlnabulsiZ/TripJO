from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..DB.database import get_db
from ..models.serializers import GetFavPlace, GetFavGuide, AddToFav, getImage
from ..DB.tables import Favorites, Place, User, Image
from ..APIs.account_info import get_user_from_token

rou = APIRouter()
auth_token = OAuth2PasswordBearer(tokenUrl="login")

@rou.post("/add_to_favorites/")
async def add_to_favorites(
    data: AddToFav,
    token: str = Depends(auth_token),
    db: Session = Depends(get_db)
):
    user = get_user_from_token(token)
    user_id = user["id"]
    
    existing_fav = db.query(Favorites).filter(
        Favorites.user_id == user_id,
        Favorites.place_id == data.place_id if data.place_id else None,
        Favorites.guide_id == data.guide_id if data.guide_id else None
    ).first()
    
    if existing_fav:
        raise HTTPException(status_code=400, detail="Item already in favorites")
    
    try:
        new_fav = Favorites(
            UserId=user_id,
            PlaceId=data.place_id,
            GuideId=data.guide_id
        )
        db.add(new_fav)
        db.commit()
        return {"message": "Added to favorites successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@rou.get("/get_favorite_places/")
async def get_favorite_places(
    token: str = Depends(auth_token),
    db: Session = Depends(get_db)
):
    user = get_user_from_token(token)
    user_id = user["id"]
    
    try:
        favorites = db.query(Favorites, Place, Image).\
            join(Place, Favorites.place_id == Place.Id).\
            join(Image, Place.id == Image.place_id).\
            filter(Favorites.user_id == user_id).\
            group_by(Place.id).\
            all()
        
        if not favorites:
            return []
        
        result = []
        for fav, place, image in favorites:
            result.append(GetFavPlace(
                name=place.name,
                city=place.city,
                rate=place.rate,
                images=[getImage(image_path=image.image_path)] if image else []
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@rou.get("/get_favorite_guides/")
async def get_favorite_guides(
    token: str = Depends(auth_token),
    db: Session = Depends(get_db)
):
    user = get_user_from_token(token)
    user_id = user["id"]
    
    try:
        guides = db.query(Favorites, User).\
            join(User, Favorites.guide_id == User.id).\
            filter(
                Favorites.user_id == user_id,
                User.role == 'guide'
            ).\
            all()
        
        return [
            GetFavGuide(
                name=f"{guide.fname} {guide.lname}",
                rate=guide.rate,
                profile_image=guide.profile_image
            )
            for _, guide in guides
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))