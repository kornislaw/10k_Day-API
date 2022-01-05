from jose import JWSError, jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

from app import schemas

SECRET_KEY = "94e8009e01b9961deed532ef826577808ed260a4bb58dba57a1ab0020e668a6c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, creds_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise creds_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise creds_exception

    return token_data


def get_current_user(token: str = Depends(oath2_scheme)):
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",
                                    headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, creds_exception)
