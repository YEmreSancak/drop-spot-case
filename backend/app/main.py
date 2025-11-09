from fastapi import FastAPI
from app.routers import auth, admin_drops, drops
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # test ortamında * kullanabiliriz
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
