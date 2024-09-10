from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.sql import func

metadata = MetaData()

item_table = Table(
    "item",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("description", String(200), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("minimum_quantity", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(),  onupdate=func.now())
)
