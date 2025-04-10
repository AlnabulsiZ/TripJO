from fastapi import APIRouter, HTTPException, Depends
from werkzeug.security import generate_password_hash
from fastapi.security import OAuth2PasswordBearer
import jwt
from ..DB.database import get_db
from ..APIs.login import key
from sqlalchemy.orm import Session
from ..models.serializers import UserRegister, GuideUpdate, OwnerUpdate
from ..DB.tables import User, Place, Image

rou = APIRouter()

auth_token = OAuth2PasswordBearer(tokenUrl="login")  


def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"]) 
        userId = payload.get()

        if userId is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return userId
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



@rou.post("/account_info/normal_user/")
def account_info_normal_user(user: UserRegister, token: str = Depends(auth_token),db: Session = Depends(get_db)):

    userId = get_user_from_token(token)

    try:
        dbUser = db.query(User).filter(User.id == userId).first() 
        if not dbUser:
            raise HTTPException(status_code=401, detail="Invalid user")
        
        else:
            if dbUser.email:
                dbUser.email = user.email

            if dbUser.password:
                dbUser.email = user.password
            
            db.commit() 

            return { 
                "First name": dbUser.fname,
                "Last name": dbUser.lname,
                "Email": dbUser.email,
                "password": dbUser.password
                }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")



@rou.post("/account_info/guide_user/")
def account_info_guide_user(guide: GuideUpdate, token: str = Depends(auth_token), db: Session = Depends(get_db)):
    
    userId = get_user_from_token(token)
    try:
        dbUser = db.query(User).filter(User.id == userId).first() 
        if not dbUser:
            raise HTTPException(status_code=404, detail="User not found")
        if dbUser.role != "guide":  
            raise HTTPException(status_code=403, detail="User is not a guide.")
        else :

            if dbUser.password:
                dbUser.name = guide.password
            
            if dbUser.email:
                dbUser.email = guide.email

            if dbUser.phone:
                dbUser.phone = guide.phone

            if dbUser.personal_image:
                dbUser.personal_image = guide.personal_image
            
            if dbUser.age:
                dbUser.age = guide.age
            
            db.commit() 

            return {
                "Fname": dbUser.fname,
                "Lname": dbUser.lname,
                "email": dbUser.email,
                "phone": dbUser.phone,
                "national_id": dbUser.national_id,
                "personal_image": dbUser.personal_image,
                "gender": dbUser.gender,
                "age": dbUser.age
                }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")


    

@rou.post("/account_info/owner/")
def account_info_owner(owner: OwnerUpdate, token: str = Depends(auth_token), db: Session = Depends(get_db)):

    userId = get_user_from_token(token) # => user id = owner id = place id 
    try:
        dbUser = db.query(User).filter(User.Id == userId).first() 
        dbPlace = db.query(Place).filter(Place.Id == userId).first()
        dbImage = db.query(Image.image_path).filter(Image.place_id == userId).all()



        if not dbUser:
            raise HTTPException(status_code=404, detail="User not found")
        if dbUser.role != "owner":
            raise HTTPException(status_code=404, detail="User is not owner")
        
        else:

            if dbPlace.name:
               dbPlace.name = owner.place.name

            if dbPlace.city:
                dbPlace.city = owner.place.city

            if dbPlace.type:
                dbPlace.type = owner.place.type

            if dbPlace.description:
                dbPlace.description = owner.place.description
            ImageList=[]
            if dbImage:
                for img in dbImage:
                    dbImage =  owner.place.images
                    ImageList.append(img)

            db.commit()        

            FullName = dbUser.fname+" "+dbUser.lname
            return{
                # owner info
                "Owner name":FullName,
                "Email": dbUser.email,
                "Phone": dbUser.phone,
                "National_id": dbUser.national_id,
                # place info
                "Place naame": dbPlace.name,
                "City": dbPlace.city,
                "Type": dbPlace.type,
                "Description": dbPlace.description,
                "Place images list": ImageList
            }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")
