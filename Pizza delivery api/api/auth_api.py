from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

from database import SessionLocal,User
from model_schema import SignUpModel, LoginModel

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.get("/")
async def hello(Authorize: AuthJWT = Depends()):
    """
    ## Sample hello world route
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return {"message": "Hello World"}

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, db: Session = Depends(get_db)):
    """
    ## Create a user
    This requires the following
    ```
    username:int
    email:str
    password:str
    is_staff:bool
    is_active:bool
    """
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email already exists")

    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the username already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    db.add(new_user)
    db.commit()

    return new_user

@auth_router.post("/signin", status_code=status.HTTP_200_OK)
async def signin(user: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    ## Login a user
    This requires
    ```
    username:str
    password:str
    ```
    and returns a token pair `access` and `refresh`
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Username Or Password")

    access_token = Authorize.create_access_token(subject=db_user.username)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username)

    response = {
        "access": access_token,
        "refresh": refresh_token
    }

    return jsonable_encoder(response)

@auth_router.get("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    """
    ## Create a fresh token
    This creates a fresh token. It requires a refresh token.
    """
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid refresh token")

    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})
