from fastapi import FastAPI
from app.APIs.register import rou as register_rou 
from app.APIs.login import rou as login_rou 
from app.APIs.account_info import rou as account_rou
from app.APIs.forgot_password import rou as forgot_rou

app = FastAPI()

app.include_router(register_rou)
app.include_router(login_rou)
app.include_router(account_rou)
app.include_router(forgot_rou)