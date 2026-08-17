from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, sms
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://192.168.68.104:5175", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(sms.router)
# app.include_router(rfid_cards.router)
# app.include_router(memberships.router)
# app.include_router(telegram.router)
# app.include_router(gates.router)