from typing import Annotated
import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()

@router.get("/basic-auth/")
def demo_basic_auth_credentials(
  credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
  return {
    "message": 'Hi!',
    "username": credentials.username,
    "password": credentials.password,
  }


usernames_to_passwords = {
  "admin": "admin",
  "user": "1234",
}

static_auth_token_to_username = {
  "2b276c7f432c884244f0a278caf0f28a": "admin",
  "adbf9f4f6b096b98799f1e42947895d3": "user",
}

def get_auth_auth_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
  unauth_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers={"WWW-Authenticate": "Basic"},
  )
  if credentials.username not in usernames_to_passwords:
    raise unauth_exc
  
  correct_password = usernames_to_passwords.get(credentials.username)
  if correct_password is None:
    raise unauth_exc

  # secrets
  if not secrets.compare_digest(
    credentials.password.encode("utf-8"),
    correct_password.encode("utf-8"),
  ): 
    raise unauth_exc
  
  return credentials.username

def get_username_by_static_auth_token(
  static_token: str = Header(alias="x-auth-token")
) -> str:
  if username := static_auth_token_to_username.get(static_token):
    return username
  
  raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="token invalid",
  )

@router.get("/basic-auth-username/")
def demo_auth_some_http_header(
  auth_username: str = Depends(get_auth_auth_username),
):
  return {
    "message": f"Hi!, {auth_username}",
    "username": auth_username,
  }

@router.get("/some-http-header-auth/")
def demo_basic_auth_username(
  username: str = Depends(get_username_by_static_auth_token),
):
  return {
    "message": f"Hi!, {username}",
    "username": username,
  }