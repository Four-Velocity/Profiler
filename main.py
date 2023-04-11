from __future__ import annotations

import json
from typing import ForwardRef, Self
from fastapi import FastAPI
from pydantic import BaseModel

# Period = ForwardRef("Period")
# class Period(BaseModel):
#     name: str
#     order: int
#     start_time: float
#     end_time: float
#     periods: list[Period] | None = None
#
#
# class Breakpoint(BaseModel):
#     group_id: str
#     item_id: str
#     type: str
#     periods: list[Period]


app = FastAPI()


@app.post("/breakpoints/")
async def add_breakpoint(breakpoint: dict):
    print(breakpoint)
    with open("./data.json", "a") as file:
        file.write(json.dumps(breakpoint))
        file.write(",\n")
    return 200

@app.get("/breakpoints/")
async def list_breakpoints():
    with open("./data.json") as file:
        data = file.read()
    if data.endswith(",\n"):
        data = data[:-2]
    dump = data + "]"

    return json.loads(dump)
