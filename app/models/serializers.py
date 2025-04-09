from pydantic import BaseModel, EmailStr, constr
from typing import List
from typing import Optional
from enum import Enum

class LoginRequest(BaseModel):
    email: str
    password: str

class getImage(BaseModel):
    image_path: str

class getComment(BaseModel):
    comment: str

class getPlaceInfo(BaseModel):
    name: str
    city: str
    type: str
    description: str
    rate: float
    images: List[getImage]
    isINFav: bool  
    comments: List[getComment]

class getGuideInfo(BaseModel):
    id: int
    Fname: str
    Lname: str 
    email: str
    phone: str
    national_id: str
    personal_image: str
    isINFav: bool

class UserRegister(BaseModel):
    Fname: str
    Lname: str
    email: EmailStr
    password: constr(min_length=6)

class PlaceRegister(BaseModel):
    name: str
    city: str
    type: str
    description: str = ""

class OwnerRegister(UserRegister):
    phone: constr(min_length=10, max_length=10)
    place: PlaceRegister

class GuideRegister(OwnerRegister):
    national_id: str
    gender: str
    age: int
    personal_image: str  
class UserUpdate(BaseModel):
    Fname: Optional[str]
    Lname: Optional[str]
    password: Optional[str]

class Gender(str, Enum):
    male = "male"
    female = "female"

class GuideUpdate(BaseModel):
    Fname: Optional[str]
    Lname: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    national_id: Optional[str]
    personal_image: Optional[str]
    gender: Optional[Gender]  
    age: Optional[int]


class ImageUpdate(BaseModel):
    image_path: Optional[str]



class PlaceUpdate(BaseModel):
    name: Optional[str]
    city: Optional[str]
    type: Optional[str]
    description: Optional[str]
    rate: Optional[float]
    images: Optional[List[ImageUpdate]]  


class OwnerUpdate(UserUpdate):
    place: Optional[PlaceUpdate]
    Fname: Optional[str]
    Lname: Optional[str]
    password: Optional[str]
    phone: Optional[str]

class getFavPlace(BaseModel):
    name: str
    city: str
    rate: float
    images: List[getImage]
   
class getFavGuide(BaseModel):
    Fname: str
    Lname: str
    rate: float    

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    reset_code: str
    new_password: str