from fastapi import FastAPI
from app.APIs.register import rou as register_rou 
from app.APIs.login import rou as login_rou 

app = FastAPI()

app.include_router(register_rou)
app.include_router(login_rou)