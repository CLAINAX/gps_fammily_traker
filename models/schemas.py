from pydantic import BaseModel

class LocationModel(BaseModel):
    lon: float  
    lat: float 

class UserModel(BaseModel):
    name: str
    age: int
    gender: bool
    location: LocationModel
