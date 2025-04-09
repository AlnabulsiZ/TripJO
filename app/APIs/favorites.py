from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..DB.database import get_db
from ..models.serializers import GetFavPlace, GetFavGuide, AddToFav, GetImage
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
        Favorites.UserId == user_id,
        Favorites.PlaceId == data.place_id if data.place_id else None,
        Favorites.GuideId == data.guide_id if data.guide_id else None
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
            join(Place, Favorites.PlaceId == Place.Id).\
            join(Image, Place.Id == Image.PlaceId).\
            filter(Favorites.UserId == user_id).\
            group_by(Place.Id).\
            all()
        
        if not favorites:
            return []
        
        result = []
        for fav, place, image in favorites:
            result.append(GetFavPlace(
                name=place.Name,
                city=place.City,
                rate=place.Rate,
                images=[GetImage(image_path=image.ImagePath)] if image else []
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
            join(User, Favorites.GuideId == User.Id).\
            filter(
                Favorites.UserId == user_id,
                User.Role == 'guide'
            ).\
            all()
        
        return [
            GetFavGuide(
                name=f"{guide.Fname} {guide.Lname}",
                rate=guide.Rate,
                profile_image=guide.ProfileImage
            )
            for _, guide in guides
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))