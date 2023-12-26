from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.supabase_client.client import supabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="get-token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    data = supabase.auth.get_user(token)
    user = data.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user