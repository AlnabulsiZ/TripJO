from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from ..DB.tables import Place, User
from ..DB.database import get_db

rou = APIRouter()

@rou.post("/search/")
def search(
    name: str = Query(None),
    type: str = Query(None),
    guide: str = Query(None),
    db: Session = Depends(get_db)
):
    try:
        if (name or type) and not guide:
            query = db.query(Place)
            if name:
                query = query.filter(Place.Name.ilike(f"%{name.strip()}%"))
            if type:
                query = query.filter(Place.Type.ilike(f"%{type.strip()}%"))

            places = query.all()
            return {
                "places": [
                    {"name": p.Name, "type": p.Type} for p in places
                ]
            }

        elif guide:
            query = db.query(User).filter(
                User.Role == "guide",
                (User.Fname.ilike(f"%{guide.strip()}%")) | (User.Lname.ilike(f"%{guide.strip()}%"))
            )
            guides = query.all()
            return {
                "guides": [
                    {"Fname": g.Fname, "Lname": g.Lname} for g in guides
                ]
            }

        else:
            raise HTTPException(status_code=400, detail="Please provide a valid search parameter.")
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@rou.post("/top_places/home/")
def get_top_places(db: Session = Depends(get_db)):
    try:
        places = (
            db.query(Place)
            .options(joinedload(Place.images))
            .order_by(Place.Rate.desc())
            .limit(10)
            .all()
        )

        result = []
        for place in places:
            image_path = place.images[0].ImagePath if place.images else "default.jpg"
            result.append({
                "name": place.Name,
                "rate": place.Rate,
                "city": place.City,
                "image_path": image_path
            })

        return {"top_places": result}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@rou.post("/top_guides/home/")
def get_top_guides(db: Session = Depends(get_db)):
    try:
        guides = (
            db.query(User)
            .filter(User.Role == "guide")
            .order_by(User.Rate.desc())
            .limit(10)
            .all()
        )
        return {
            "top_guides": [
                {"Fname": g.Fname, "personal_image": g.PersonalImage} for g in guides
            ]
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
