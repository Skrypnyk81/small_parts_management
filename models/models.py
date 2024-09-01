from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime

metadata = MetaData()

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("description", String(200), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("minimum_quantity", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False),
)
