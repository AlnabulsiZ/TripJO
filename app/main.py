from fastapi import FastAPI
from app.APIs.register import rou as register_rou 

app = FastAPI()





app.include_router(register_rou)