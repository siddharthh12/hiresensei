from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import user_collection, user_helper
from app.models.user import UserCreate, User, Token, UserInDB
from app.core.security import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from bson.objectid import ObjectId
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    if "password" in user_data:
        del user_data["password"]
        
    try:
        user_in_db = UserInDB(
            **user_data,
            hashed_password=hashed_password
        )
    except Exception as e:
        print(f"Error creating UserInDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )
    
    new_user = await user_collection.insert_one(user_in_db.dict())
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
