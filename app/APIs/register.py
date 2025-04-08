import sqlite3
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from ..DB.database import get_db
from ..models.BMClasses import UserRegister, OwnerRegister, GuideRegister
import os
from werkzeug.security import generate_password_hash
from typing import List
from sqlalchemy.orm import Session
from ..DB.tables import Place, Image, User


rou = APIRouter()
    

@rou.post("/register/user/")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
     
    try:
        new_user = User(
            Fname=user.Fname,
            Lname=user.Lname,
            Email=user.email,
            Password=generate_password_hash(user.password),
            Role="user"
        )
        db.add(new_user)
        db.commit()
        return {"message": "User registered successfully"}
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        db.close()

@rou.post("/register/owner/")
async def register_owner(owner: OwnerRegister, images: List[UploadFile] = File(...),db: Session = Depends(get_db)):

    if len(images) < 5:
        raise HTTPException(status_code=400, detail="You must upload at least 5 images")

    try:
        new_owner = User(
            Fname=owner.Fname,
            Lname=owner.Lname,
            Email=owner.email,
            Phone=owner.phone,
            Password=generate_password_hash(owner.password),
            Role="owner"
        )
        db.add(new_owner)
        db.commit()
        owner_id = new_owner.Id  

        new_place = Place(
            Name=owner.place.name,
            City=owner.place.city,
            Type=owner.place.type,
            Description=owner.place.description,
            OwnerId=owner_id
        )
        db.add(new_place)
        db.commit()
        place_id = new_place.Id  

        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        for image in images:
            image_path = f"uploads/{image.filename}"
            with open(image_path, "wb") as f:
                f.write(await image.read())

            new_image = Image(
                PlaceId=place_id,
                ImagePath=image_path,
                IsMain=False  
            )
            db.add(new_image)

        db.commit()
        return {"message": "Owner and place registered successfully", "owner_id": owner_id, "place_id": place_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email or Phone already exists")
    finally:
        db.close()

@rou.post("/register/guide/")
async def register_guide(guide: GuideRegister, image: UploadFile = File(...),db: Session = Depends(get_db)):
    if not os.path.exists("uploads/guides"):
        os.makedirs("uploads/guides")

    image_path = f"uploads/guides/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())

    try:
        new_guide = User(
            Fname=guide.Fname,
            Lname=guide.Lname,
            Email=guide.email,
            Phone=guide.phone,
            Password= generate_password_hash(guide.password),
            Role="guide",
            NationalId=guide.national_id,
            PersonalImage=guide.personal_image,
            Gender=guide.gender,
            Age=guide.age
        )
        db.add(new_guide)
        db.commit()
        guide_id = new_guide.Id  

        new_image = Image(
            PlaceId=None,  
            ImagePath=image_path,
            IsMain=True  
        )
        db.add(new_image)
        db.commit()

        return {"message": "Guide registered successfully", "guide_id": guide_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email, Phone, or National ID already exists")
    finally:
        db.close()
