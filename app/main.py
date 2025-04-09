from fastapi import FastAPI
from app.APIs.register import rou as register_rou 
from app.APIs.login import rou as login_rou 
from app.APIs.account_info import rou as account_rou
from app.APIs.forgot_password import rou as forgot_rou
from app.APIs.show_place_for_user import rou as show_place_rou
from app.APIs.show_guide_for_user import rou as show_guide_rou
from app.APIs.favorites import rou as favorites_rou

app = FastAPI()

app.include_router(register_rou)
app.include_router(login_rou)
app.include_router(account_rou)
app.include_router(forgot_rou)
app.include_router(show_place_rou)
app.include_router(show_guide_rou)
app.include_router(favorites_rou)