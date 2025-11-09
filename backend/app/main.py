from fastapi import FastAPI
from app.routers import auth, admin_drops, drops
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin_drops.router)
app.include_router(drops.router)

@app.get("/")
def root():
    return {"message": "DropSpot Backend API running"}
