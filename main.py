from datetime import datetime
from fastapi import FastAPI, UploadFile, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.database import get_async_session
from item.schemas import ItemCreate
from models.models import item_table
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession



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

@app.get("/item", name="search_item")
async def read_item(request: Request, item_name: str, db: AsyncSession = Depends(get_async_session)):
    query = select(item_table).where(item_table.c.name == item_name)
    result = await db.execute(query)
    item = result.first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_dict = dict(zip(item_table.c.keys(), item))
    return templates.TemplateResponse(
        "item_detail.html",
        {"request": request, "item": item_dict}
    )

@app.post("/item_add")
async def add_item(item_data: ItemCreate, db: AsyncSession = Depends(get_async_session)):
    new_item = insert(item_table).values(**item_data.model_dump())
    await db.execute(new_item)
    await db.commit()

    query = select(item_table).order_by(item_table.c.id.desc()).limit(1)
    result = await db.execute(query)
    insered_item = result.scalar_one()
    return {"message": "Item added successfully", "item": insered_item}

