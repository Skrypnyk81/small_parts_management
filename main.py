from fastapi import FastAPI, UploadFile, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.database import get_async_session
from item.schemas import ItemCreate, ItemAdd
from models.models import item_table
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.get("/home", response_class=HTMLResponse)
async def get_home(
    request: Request,
):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse)
async def get_upload(
    request: Request,
):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def read_item(
    request: Request,
    barCode: Annotated[str, Form()],
    db: AsyncSession = Depends(get_async_session),
):
    context = {"request": request}
    query = select(item_table).where(item_table.c.name == barCode)
    result = await db.execute(query)
    item = result.first()

    if item is None:
        context["error"] = "Articolo non trovato"
        return templates.TemplateResponse("upload.html", context)

    item_dict = dict(zip(item_table.c.keys(), item))
    return templates.TemplateResponse(
        "item_detail.html", {"request": request, "item": item_dict}
    )


@app.post("/item_result", response_class=HTMLResponse)
async def add_item(
    request: Request,
    item: Annotated[ItemAdd, Depends(ItemAdd.as_form)],
):
    return templates.TemplateResponse(
        "item_to_db.html", {"request": request, "item_add": item}
    )


@app.post(
    "/item_add_to_db",
    response_class=HTMLResponse,
    name="item_add_to_db",
)
async def add_item_to_db(
    request: Request,
    item_add: Annotated[ItemAdd, Depends(ItemAdd.as_form)],
    db: AsyncSession = Depends(get_async_session),
):
    query = select(item_table).where(item_table.c.name == item_add.name)
    result = await db.execute(query)
    item = result.first()
    new_quantity = item.quantity + item_add.quantity
    update_query = (
        update(item_table)
        .where(item_table.c.name == item_add.name)
        .values(quantity=new_quantity)
    )

    await db.execute(update_query)
    await db.commit()

    query = select(item_table).where(item_table.c.name == item_add.name)
    result = await db.execute(query)
    updated_item = result.first()

    return templates.TemplateResponse(
        "add_result.html", {"request": request, "item": updated_item}
    )


@app.get("/download", response_class=HTMLResponse)
async def get_download(
    request: Request,
):
    return templates.TemplateResponse("download.html", {"request": request})


@app.post("/item_add")
async def create_item(
    item_data: ItemCreate, db: AsyncSession = Depends(get_async_session)
):
    new_item = insert(item_table).values(**item_data.model_dump())
    await db.execute(new_item)
    await db.commit()

    query = select(item_table).order_by(item_table.c.id.desc()).limit(1)
    result = await db.execute(query)
    insered_item = result.scalar_one()
    return {"message": "Item added successfully", "item": insered_item}
