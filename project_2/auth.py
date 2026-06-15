from fastapi import Form, APIRouter

router = APIRouter()

@router.post('/login', status_code=200)
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "message": "Login successful"}