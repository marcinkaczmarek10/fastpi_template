from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.api.auth.models import user_pydantic, User, user_exclude_read_only, user_login
from src.api.auth.crypto import check_password_hash, get_password_hash, create_access_token
from src.api.auth.validators import validate_password, validate_email

auth = APIRouter()


@auth.post("/register", response_class=JSONResponse)
async def post_register(user: user_exclude_read_only):
    if not user.password or not user.email:
        return JSONResponse(content={"message": "Bad request"}, status_code=400)
    if not validate_password(user.password) or not validate_email(user.email):
        return JSONResponse(content={"message": "Bad request"}, status_code=400)
    user_dict = user.dict(exclude_unset=True)
    hashed_password = get_password_hash(user_dict.get("password"))
    user_dict.update(password=hashed_password)
    new_user = await User.create(**user_dict)
    if new_user:
        return {}


@auth.post("/login", response_class=JSONResponse)
async def post_login(credentials: user_login):
    if not credentials.password or not credentials.email:
        return JSONResponse(content={"message": "Bad request"}, status_code=400)
    if not validate_password(credentials.password) or not validate_email(credentials.email):
        return JSONResponse(content={"message": "Bad request"}, status_code=400)
    user = await User.get(email=credentials.email)
    if check_password_hash(credentials.password, user.password):
        token = create_access_token({"user": user.email})
        return JSONResponse(content={"token": token}, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Wrong credentials!")


@auth.get("/users")
async def get_users():
    return await user_pydantic.from_queryset(User.all())


@auth.get("/user/{user_id}", response_model=user_pydantic)
async def get_user(user_id: int):
    return await user_pydantic.from_queryset_single(User.get(id=user_id))
