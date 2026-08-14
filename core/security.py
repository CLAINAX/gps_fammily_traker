import uuid

MASTER_TOKEN = "abc_123"
USER_TOKENS = {}  

def rotate_all_tokens():

    global MASTER_TOKEN, USER_TOKENS
    MASTER_TOKEN = str(uuid.uuid4())
    

    for user_id in USER_TOKENS:
        USER_TOKENS[user_id] = str(uuid.uuid4())

def get_master_token() -> str:
    return MASTER_TOKEN

def get_user_token(user_id: str) -> str:

    if user_id not in USER_TOKENS:
        USER_TOKENS[user_id] = str(uuid.uuid4())
    return USER_TOKENS[user_id]

def is_master_valid(token: str) -> bool:
    return token == MASTER_TOKEN

def is_user_valid(user_id: str, token: str) -> bool:

    if token == MASTER_TOKEN:
        return True
    return USER_TOKENS.get(user_id) == token



SYSTEM_STATUS = 0  #ok__Z__

def set_status(val: int):
    global SYSTEM_STATUS
    SYSTEM_STATUS = val

def get_status() -> int:
    return SYSTEM_STATUS