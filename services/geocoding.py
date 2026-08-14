import requests

def get_address(lat: float, lon: float) -> str:
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {

        "User-Agent": "Live360Clone_ModularApp/1.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Direction not found!-_-")
    except requests.RequestException:
        pass
    
    return "Dirección no disponible"