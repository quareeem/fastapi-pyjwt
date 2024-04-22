import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import User, get_db
from src.config import settings
from src.utils import decode_jwt, encode_jwt

app = FastAPI()
security = HTTPBearer()


class Login(BaseModel):
    username: str
    password: str


@app.post("/user_login")
def login_user(login: Login, db: Session = Depends(get_db)):
    """
    Функция проверяет пользователя и выдает JWT токен
    """

    user = db.query(User).filter(User.username == login.username).first()
    if not user or user.password != login.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token_data = {"sub": user.username}
    private_key = settings.auth_jwt.private_key_path.read_text()
    access_token = encode_jwt(token_data, private_key, settings.auth_jwt.algorithm)

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        decoded_token = decode_jwt(token.credentials)
        return decoded_token
    except PyJWTError as e:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@app.get("/protected")
def read_protected_data(current_user: dict = Depends(get_current_user)):
    """
    Защищенный эндпоинт, который требует наличия действительного JWT для доступа
    """
    return {"message": f"Hello {current_user['sub']}, you are authenticated!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
