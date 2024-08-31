from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.get("/home/", response_class=HTMLResponse)
async def get_home(request: Request,):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/upload/", response_class=HTMLResponse)
async def get_upload(request: Request,):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )

@app.get("/download/", response_class=HTMLResponse)
async def get_download(request: Request,):
    return templates.TemplateResponse(
        "download.html",
        {"request": request}
    )