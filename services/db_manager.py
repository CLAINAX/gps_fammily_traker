import json
import os
import uuid
from datetime import datetime, timezone
from services.geocoding import get_address
import math


def _obtener_distancia_mts(lat1, lon1, lat2, lon2):
    R = 6371000 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class PartitionDB:
    def __init__(self, partitions_dir="data/partitions"):
        self.dir = partitions_dir
        os.makedirs(self.dir, exist_ok=True)

    def get_path(self, user_id: str) -> str:
        first_char = user_id[0].lower()
        return os.path.join(self.dir, f"{first_char}.json")

    def load(self, path: str) -> dict:
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save(self, path: str, data: dict):
        with open(path, "w") as f:
            json.dump(data, f, indent=3)

db = PartitionDB()


def create_user(user_data: dict) -> str:
    new_id = str(uuid.uuid4())
    path = db.get_path(new_id)
    data = db.load(path)
    
    while new_id in data:
        new_id = str(uuid.uuid4())
        path = db.get_path(new_id)
        data = db.load(path)
        
    lat = user_data["location"]["lat"]
    lon = user_data["location"]["lon"]
    address = get_address(lat, lon)
    
    geojson_feature = {
        "type": "Feature",
        "id": new_id,
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat] 
        },
        "properties": {
            "name": user_data["name"],
            "age": user_data["age"],
            "gender": user_data["gender"],
            "address": address,
            "history": [
                {
                    "coordinates": [lon, lat],
                    "time": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
    }
        
    data[new_id] = geojson_feature
    db.save(path, data)
    return new_id

def update_user_location(user_id: str, lat: float, lon: float) -> bool:
    path = db.get_path(user_id)
    data = db.load(path)
    
    if user_id not in data:
        return False
        
    now = datetime.now(timezone.utc)
    data[user_id]["geometry"]["coordinates"] = [lon, lat]

    data[user_id]["properties"]["address"] = get_address(lat, lon)
    
    nueva_posicion = {
        "coordinates": [lon, lat],
        "time": now.isoformat()
    }
    data[user_id]["properties"]["history"].append(nueva_posicion)
    
    historial_limpio = []
    for punto in data[user_id]["properties"]["history"]:
        try:
            punto_tiempo = datetime.fromisoformat(punto["time"])
            if (now - punto_tiempo).days <= 30:
                historial_limpio.append(punto)
        except ValueError:
            pass
            
    data[user_id]["properties"]["history"] = historial_limpio
    db.save(path, data)
    return True

def get_all_users_geojson() -> dict:
    features = []
    if os.path.exists(db.dir):
        for filename in os.listdir(db.dir):
            if filename.endswith(".json"):
                path = os.path.join(db.dir, filename)
                partition_data = db.load(path)
                features.extend(list(partition_data.values()))
                
    return {
        "type": "FeatureCollection",
        "features": features
    }