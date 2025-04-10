from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from ..models.serializers import getPlaceInfo
from sqlalchemy.exc import SQLAlchemyError
from ..DB.tables import Place
from ..DB.database import get_db

rou = APIRouter()

jordan_governorates = [
    "Amman", "Zarqa", "Irbid", "Balqa", "Mafraq",
    "Karak", "Tafilah", "Ma'an", "Aqaba", "Jerash",
    "Ajloun", "Madaba"
]

@rou.post("/places/by_city/")
def get_places_by_city(db: Session = Depends(get_db)):
    try:
        places = (
            db.query(Place)
            .options(joinedload(Place.images))
            .all()
        )

        grouped_places = {city: [] for city in jordan_governorates}

        for place in places:
            city = place.City
            image_path = place.images[0].ImagePath if place.images else "default.jpg"

            place_data = {
                "name": place.Name,
                "rate": place.Rate,
                "image_path": image_path
            }

            if city in grouped_places:
                grouped_places[city].append(place_data)
            else:
                grouped_places.setdefault(city, []).append(place_data)

        return {"places_by_city": grouped_places}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
