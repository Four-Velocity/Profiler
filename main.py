from __future__ import annotations

import json
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Settings(BaseSettings):
    database_url: str


settings = Settings()


class Period(BaseModel):
    name: str
    verbose: str | None = None
    start_time: float
    end_time: float

    class Config:
        schema_extra = {
            "example": {
                "name": "some_name",
                "verbose": "Some Task (Profiling execution)",
                "start_time": 1681282223.053712,
                "end_time": 1681283174.048276,
            }
        }


class Breakpoint(BaseModel):
    group_id: str = Field()
    item_id: str
    type: str | None = None
    periods: list[Period]

    class Config:
        schema_extra = {
            "example": {
                "group_id": "b4827861-48cb-41e0-a907-471f4b2b1e27",
                "item_id": "abC=12df",
                "type": "success",
                "periods": [
                    {"name": "total", "start_time": 1681281218.3709528, "end_time": 1681283174.048276,},
                    {"name": "sub_task_a", "start_time": 1681281218.3709528, "end_time": 1681282223.053712,},
                    {"name": "sub_task_b", "verbose": "Task B (Optional)", "start_time": 1681282223.053712, "end_time": 1681283174.048276,},
                ]
            }
        }


class BreakpointResponse(Breakpoint):
    id: str = Field(default_factory=str, alias="_id")


app = FastAPI()
client = AsyncIOMotorClient(settings.database_url)


def get_db():
    db = client.app
    return db


@app.post("/breakpoints/", response_model=Breakpoint, tags=["Breakpoints"])
async def add_breakpoint(breakpoint: Breakpoint, db: AsyncIOMotorDatabase = Depends(get_db)):
    collection = db.default
    results = await collection.insert_one(breakpoint.dict())
    return Breakpoint


@app.get("/breakpoints/", response_model=list[Breakpoint], tags=["Breakpoints"])
async def list_breakpoints(db: AsyncIOMotorDatabase = Depends(get_db)):
    collection = db.default
    # results = await collection.find({}).to_list(length=None)
    results = [i async for i in collection.find({})]
    return results

