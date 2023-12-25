import logging
from typing import Annotated, List, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user
from app.models.common_models import User, Resume
from app.supabase_client.client import supabase
from app.handlers.resume_handler import CreateResumeParams, create_new_resume, find_all_resumes, process_job_for_resume, \
    AnalyseJobForResumeParams

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler("resume_logger.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Cver": "World"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.post("/resume", response_model=Resume)
async def create_resume(params: CreateResumeParams, current_user: Annotated[User, Depends(get_current_user)]):
    """ creates a new resume called after uploading to bucket"""
    return create_new_resume(current_user, params)


@app.post("/job/process")
async def create_resume(params: AnalyseJobForResumeParams, current_user: Annotated[User, Depends(get_current_user)]):
    return process_job_for_resume(current_user, params)


@app.get("/resumes", response_model=Optional[List[Resume]])
async def list_resume(current_user: Annotated[User, Depends(get_current_user)]):
    """ list all resumes for user """
    return find_all_resumes(current_user)


@app.post("/get-token")
async def get_login_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    data = supabase.auth.sign_in_with_password({"email": form_data.username, "password": form_data.password})
    token, token_type = data.session.access_token, data.session.token_type
    return {"access_token": token, "token_type": token_type}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
