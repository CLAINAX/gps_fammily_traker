from api.routes import read_root
from fastapi import HTTPException

def test_read_root():
    assert read_root("fakeUser123") is HTTPException
    assert read_root("14bed1d4-c363-414b-b422-8bd60685e8c5") == True

def __init__():
    test_read_root()