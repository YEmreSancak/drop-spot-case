from fastapi import FastAPI
from app.routers import auth, admin_drops, drops

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin_drops.router)
app.include_router(drops.router)

@app.get("/")
def root():
    return {"message": "DropSpot Backend API running"}
