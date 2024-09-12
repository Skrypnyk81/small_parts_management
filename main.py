from fastapi import FastAPI, UploadFile, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.database import get_async_session
from item.schemas import ItemCreate
from models.models import item_table
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated




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


@app.post("/upload", response_class=HTMLResponse)
async def read_item(request: Request, barCode: Annotated[str, Form()], db: AsyncSession = Depends(get_async_session)):
    context = {"request": request}
    query = select(item_table).where(item_table.c.name == barCode)
    result = await db.execute(query)
    item = result.first()

    if item is None:
        context["error"] = "Articolo non trovato"
        return templates.TemplateResponse("upload.html", context)
    
    item_dict = dict(zip(item_table.c.keys(), item))
    return templates.TemplateResponse(
        "item_detail.html",
        {"request": request, "item": item_dict}
    )


@app.get("/download", response_class=HTMLResponse)
async def get_download(request: Request,):
    return templates.TemplateResponse(
        "download.html",
        {"request": request}
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

