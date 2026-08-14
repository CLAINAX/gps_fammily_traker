import requests
from core.security import set_status


ROBOT_NAMES = ["RobotAlpha", "RobotBeta", "RobotGamma"]

def run_all_tests():
    base_url = "http://127.0.0.1:8000"
    
    try:

        res = requests.get(f"{base_url}/refresh/?secret=max123")
        if res.status_code != 200: 
            raise Exception("Fallo al obtener Token Maestro")
        master_token = res.json()
        headers = {"Authorization": f"Bearer {master_token}"}


        res = requests.get(f"{base_url}/users", headers=headers)
        if res.status_code != 200: 
            raise Exception("Fallo al leer usuarios")
        
        geojson = res.json()
        features = geojson.get("features", [])
        
        target_user = None
        for feature in features:
            name = feature.get("properties", {}).get("name")
            if name in ROBOT_NAMES:
                target_user = feature
                break

        if not target_user:
            set_status(0)
            return

        user_id = target_user["id"]

        loc_data = {"lat": 40.4168, "lon": -3.7038}
        res = requests.put(f"{base_url}/update-location/{user_id}", json=loc_data)
        if res.status_code != 200: 
            raise Exception("Fallo al actualizar GPS del usuario fijo")


        res = requests.get(f"{base_url}/api/{user_id}", headers=headers)
        if res.status_code != 200: 
            raise Exception("Fallo al leer los datos específicos del usuario")
        set_status(0)
    except Exception as e:
        print(f"TEST AUTOMÁTICO FALLIDO: {e}")
        set_status(1)