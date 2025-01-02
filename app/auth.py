from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from .models import User

SECREY_KEY = "your_secret_key"
ALGONITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

# creat JWT Token
def create_access_token(
        data: dict,
        expiresDelta: timedelta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTE)):
    toEncode = data.copy()
    expire = datetime.utcnow() + expiresDelta
    toEncode.update({"exp": expire})
    encodeJwt = jwt.encode(toEncode, SECREY_KEY, algorithm = ALGONITHM)
    return encodeJwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECREY_KEY, algorithms = [ALGONITHM])
        return payload
    except JWTError:
        return None

# login route to issue JWT
router = APIRouter()
@router.post("/token")
async def login_for_access_token(user: User):
    # todo: check user if exist and validate password
    accessToken = create_access_token(data={"sub": user.username})
    return {"accessToken": accessToken, "tokenType": "bearer"}

def get_current_user(token: str):
    user = verify_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user