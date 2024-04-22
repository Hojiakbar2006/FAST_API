from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth, models, schemas, security
from app.database import get_db

router = APIRouter()


@router.post("/register/", response_model=schemas.UserInDBBase)
async def register_user(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already registered")
    db_user = db.query(models.User).filter(
        models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        **user_in.dict(exclude={"password"}), hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.get_user(db, username=form_data.username)
    if not user or not security.pwd_context.verify(
            form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.TOKEN_EXPIRE_TIME)
    access_token = security.create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "beare"}


@router.get("/conversation")
async def read_conversation(current_user: schemas.UserInDB = Depends(auth.get_current_user)):
    return {
        "conversation": "This is a secure conversation!",
        "current_user": current_user
    }
