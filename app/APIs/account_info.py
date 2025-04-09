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
        dbUser = db.query(User).filter(User.Id == userId).first() 
        if not dbUser:
            raise HTTPException(status_code=401, detail="Invalid user")
        
        else:
            if dbUser.Email:
                dbUser.Email = user.email

            if dbUser.Password:
                dbUser.Email = user.password
            
            db.commit() 

            return { 
                "First name": dbUser.Fname,
                "Last name": dbUser.Lname,
                "Email": dbUser.Email,
                "password": dbUser.Password
                }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")



@rou.post("/account_info/guide_user/")
def account_info_guide_user(guide: GuideUpdate, token: str = Depends(auth_token), db: Session = Depends(get_db)):
    
    userId = get_user_from_token(token)
    try:
        dbUser = db.query(User).filter(User.Id == userId).first() 
        if not dbUser:
            raise HTTPException(status_code=404, detail="User not found")
        if dbUser.Role != "guide":  
            raise HTTPException(status_code=403, detail="User is not a guide.")
        else :

            if dbUser.Password:
                dbUser.Name = guide.password
            
            if dbUser.Email:
                dbUser.Email = guide.email

            if dbUser.Phone:
                dbUser.Phone = guide.phone

            if dbUser.PersonalImage:
                dbUser.PersonalImage = guide.personal_image
            
            if dbUser.Age:
                dbUser.Age = guide.age
            
            db.commit() 

            return {
                "Fname": dbUser.Fname,
                "Lname": dbUser.Lname,
                "email": dbUser.Email,
                "phone": dbUser.Phone,
                "national_id": dbUser.NationalId,
                "personal_image": dbUser.PersonalImage,
                "gender": dbUser.Gender,
                "age": dbUser.Age
                }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")


    

@rou.post("/account_info/owner/")
def account_info_owner(owner: OwnerUpdate, token: str = Depends(auth_token), db: Session = Depends(get_db)):

    userId = get_user_from_token(token) # => user id = owner id = place id 
    try:
        dbUser = db.query(User).filter(User.Id == userId).first() 
        dbPlace = db.query(Place).filter(Place.Id == userId).first()
        dbImage = db.query(Image.ImagePath).filter(Image.placeId == userId).all()



        if not dbUser:
            raise HTTPException(status_code=404, detail="User not found")
        if dbUser.Role != "owner":
            raise HTTPException(status_code=404, detail="User is not owner")
        
        else:

            if dbPlace.Name:
               dbPlace.Name = owner.place.name

            if dbPlace.City:
                dbPlace.City = owner.place.city

            if dbPlace.Type:
                dbPlace.Type = owner.place.type

            if dbPlace.Description:
                dbPlace.Description = owner.place.description
            ImageList=[]
            if dbImage:
                for img in dbImage:
                    dbImage =  owner.place.images
                    ImageList.append(img)

            db.commit()        

            FullName = dbUser.Fname+" "+dbUser.Lname
            return{
                # owner info
                "Owner name":FullName,
                "Email": dbUser.Email,
                "Phone": dbUser.Phone,
                "National_id": dbUser.NationalId,
                # place info
                "Place naame": dbPlace.Name,
                "City": dbPlace.City,
                "Type": dbPlace.Type,
                "Description": dbPlace.Description,
                "Place images list": ImageList
            }
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")
