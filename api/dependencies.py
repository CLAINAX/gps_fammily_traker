from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import is_master_valid, is_user_valid

bearer = HTTPBearer()

def verify_master(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if not is_master_valid(credentials.credentials):
        raise HTTPException(status_code=401, detail="Token maestro inválido")
    return credentials.credentials


def verify_user(user_id: str, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if not is_user_valid(user_id, credentials.credentials):
        raise HTTPException(status_code=401, detail="Token de usuario inválido")
    return credentials.credentials