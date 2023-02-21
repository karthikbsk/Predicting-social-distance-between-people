import uvicorn
from fastapi import FastAPI
from fastapi import File,UploadFile,utils
from fastapi import staticfiles, BackgroundTasks
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from verify_params import  *
from main import *


###Initializaing the class instance

class social(BaseModel):
    file_url : str
    
#_______________________creating fastapi____and creating static(input/output)folders_____    
app = FastAPI()

VerifyValidateParams.create_folders_if_doesnot_exist()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/input", StaticFiles(directory="static/input"), name="static")

@app.post('/social_distancing')
##________________       _______for background task starting____

# async def bg(input_args:social,backgroundtasks:BackgroundTasks):
#     backgroundtasks.add_task(upload_video_url,input_args)
#     return "BACKGROUND TASK ADDED AND MAKING DETECTION FROM VIDEO"




async def upload_video_url(input_args:social):
    
    url_to_process =input_args.file_url
    
    response_final =  social_distancing(url_to_process)
    return response_final

    
    # return final_response