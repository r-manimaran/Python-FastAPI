from typing import Annotated, List
from fastapi import FastAPI, status, Depends, BackgroundTasks, HTTPException
from sqlmodel import Field, SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select as async_select
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield # Yield control to the application
    # If there are any shutdown tasks, they can be added here
    # For example you might want to close async engine connections

app = FastAPI(lifespan=lifespan)

#Async database Setup here
DATABASE_URL = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create the Models
# --------------------------------------------------------------------
class ItemBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ItemRead(ItemBase):
    id: int




# Service Layer
# --------------------------------------------------------------------
class ItemService:
    async def create_item(self, item:ItemCreate, db:Session) -> Item:
        db_Item = Item(title=item.title, description=item.description)
        db.add(db_Item)
        await db.commit()
        await db.refresh(db_Item)
        return db_Item
    
    async def get_item(self, item_id:int, db:Session) -> Item:
        async with db as session:
            statement = async_select(Item).where(Item.id == item_id)
            result = await session.execute(statement)
            item = result.scalar()
            return item
    
    async def get_items(self, db:Session) -> List[Item]:
        async with db as session:
            statement = async_select(Item)
            result = await session.execute(statement)
            items = result.scalars().all()
            return items

# Dependency
# --------------------------------------------------------------------

def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_item_service():
    return ItemService()

db_dependency = Annotated[Session, Depends(get_db)]
item_service_dependency = Annotated[ItemService, Depends(get_item_service)]

# API Layer
# --------------------------------------------------------------------

@app.post("/items/", status_code=status.HTTP_201_CREATED, response_model=ItemRead)
async def create_item(item: ItemCreate, background_tasks:BackgroundTasks, item_service:item_service_dependency, db:db_dependency):
    db_item = await item_service.create_item(item, db)
    background_tasks.add_task(log_operation, item_id=db_item.id)
    return db_item

# return List of items
@app.get("/items/", response_model=List[ItemRead])
async def read_items(item_service:item_service_dependency, db:db_dependency):
    items = await item_service.get_items(db)
    return items

# return single item
@app.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, item_service:item_service_dependency, db:db_dependency):
    item = await item_service.get_item(item_id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def log_operation(item_id:int):
    print(f"Item created with id: {item_id}")


