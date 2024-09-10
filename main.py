from datetime import datetime
from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.database import get_async_session
from item.schemas import ItemCreate
from models.models import item_table
from sqlalchemy import insert, select



app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.get("/home", response_class=HTMLResponse)
async def get_home(request: Request,):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/upload", response_class=HTMLResponse)
async def get_upload(request: Request,):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )

@app.get("/download", response_class=HTMLResponse)
async def get_download(request: Request,):
    return templates.TemplateResponse(
        "download.html",
        {"request": request}
    )

@app.get("/item/{item_name}")
async def read_item(item_name: str, db: Session = Depends(get_async_session)):
    item = db.query(item).filter(item.name == item_name).first()
    return {"item_id": item}

@app.post("/item_add")
async def add_item(item_data: ItemCreate, db: Session = Depends(get_async_session)):
    new_item = insert(item_table).values(**item_data.model_dump())
    await db.execute(new_item)
    await db.commit()

    query = select(item_table).order_by(item_table.c.id.desc()).limit(1)
    result = await db.execute(query)
    insered_item = result.scalar_one()
    return {"message": "Item added successfully", "item": insered_item}
