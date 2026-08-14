from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from models.schemas import UserModel, LocationModel
from services import db_manager
from core import security
from api.dependencies import verify_master, verify_user
import os

router = APIRouter()

@router.get("/")
def ping():
    return {"healthy": True}
@router.get("/api/{user_id}")
def read_root(user_id: str, token: str = Depends(verify_user)):
    user = db_manager.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/refresh/")
def get_new_token(secret: str, user_id: str = None):
    if secret != "max123":
        raise HTTPException(status_code=403, detail="Contraseña denegada")
    if user_id:
        return security.get_user_token(user_id)
    return security.get_master_token()

@router.post("/create-user")
def create_user(user: UserModel, token: str = Depends(verify_master)):
    new_id = db_manager.create_user(user.model_dump())
    return {"status": "created", "new_id": new_id}

@router.put("/update-location/{user_id}")
def update_location(user_id: str, loc: LocationModel):
    success = db_manager.update_user_location(user_id, loc.lat, loc.lon)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"status": "Ubicación guardada"}

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: str, token: str = Depends(verify_master)):
    success = db_manager.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"deleted": user_id}

@router.get("/users")
def get_all_users(token: str = Depends(verify_master)):
    return db_manager.get_all_users_geojson()

@router.get("/map", response_class=HTMLResponse)
def get_map():
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "map.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@router.get("/")
def ping():
    return {"healthy": True}


@router.get("/status")
def get_system_status():
    return {"status": security.get_status()}
