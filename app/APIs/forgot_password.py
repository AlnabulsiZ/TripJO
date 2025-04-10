import random
import string
import smtplib
from fastapi import APIRouter, HTTPException, Depends
from werkzeug.security import generate_password_hash
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..DB.database import get_db
import os
from ..models.serializers import ForgotPasswordRequest, ResetPasswordRequest
from dotenv import load_dotenv
from ..APIs.account_info import get_user_from_token
from ..DB.tables import User

rou = APIRouter()
auth_token = OAuth2PasswordBearer(tokenUrl="login")  

def generate_reset_code():
    return ''.join(random.choices(string.digits, k=4))

def validate_password(new_password: str):
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    return new_password
    
def send_reset_email(email: str, reset_code: str):
    load_dotenv()  
    sender = os.getenv("EMAIL_SENDER")  
    sender_password = os.getenv("EMAIL_PASSWORD")  
    message = f"Your password reset code is: {reset_code}"

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(sender, sender_password)
        s.sendmail(sender, email, message)
        s.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False  


@rou.post("/forgot_password")
def forgot_password(data: ForgotPasswordRequest, token: str = Depends(auth_token),db: Session = Depends(get_db)):
    userId = get_user_from_token(token)
    

    try:
        dbUser = db.query(User).filter(User.id == userId).first() 

        if not dbUser:
            raise HTTPException(status_code=401, detail="Invalid user")
        else:
            reset_code = generate_reset_code()
            dbUser.reset_code = reset_code

            if send_reset_email(data.email, reset_code):
                return {"message": "Reset code sent to your email", "status": "success"}
            else:
                raise HTTPException(status_code=500, detail="Failed to send email")
    except:
        raise HTTPException(status_code=404, detail="Email not found in our records")





@rou.post("/reset_password")
def reset_password(data: ResetPasswordRequest, token: str = Depends(auth_token),db: Session = Depends(get_db)):
   
    userId = get_user_from_token(token)

    try:
        dbUser = db.query(User.reset_code,User.role,User.password).filter(User.id == userId).first()
        validated_password=""
        if dbUser:
            new_password = data.new_password
            validated_password = validate_password(new_password)

        hashed_password = generate_password_hash(validated_password)
        dbUser.reset_code = None
        dbUser.password = hashed_password

        return{
            "New password" : dbUser.password,
            "message": "Password reset successfully"
        }
        

    
    except Exception as e:
        raise HTTPException(status_code=402, detail="Fail, Try again")    


    
    


   