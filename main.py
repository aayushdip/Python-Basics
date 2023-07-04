from fastapi import FastAPI,Query,Form,File, UploadFile, HTTPException
from enum import Enum
from typing import Optional,Annotated
from pydantic import BaseModel

class Option(str,Enum):
    RECEIVED = 'RECEIVED'
    CREATED = 'CREATED'
    CREATE_ERROR = 'CREATE_ERROR'

item_data = [
    {
        "name": "Item 1",
        "description": "This is item 1",
        "price": 19.99,
        "tax": 2.0,
        "tags": {"tag1", "tag2"},
        "status": 'RECEIVED'
    },
    {
        "name": "Item 2",
        "description": "This is item 2",
        "price": 12.5,
        "tags": {"tag3", "tag4"},
        "status": 'CREATED'
    },
    {
        "name": "Item 3",
        "price": 9.99,
        "tags": {"tag1"},
        "status": 'CREATED'
    },
    {
        "name": "Item 4",
        "description": "This is item 4",
        "price": 7.25,
        "tags": {"tag2", "tag4"},
        "status": 'RECEIVED'
    },
    {
        "name": "Item 5",
        "price": 15.0,
        "status": 'CREATE_ERROR'
    }
]


class Item(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    status : Option = None
    
app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int | str):
    return{"item_id":item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/status/{status}")
async def get_status(
    status:Option, description : Annotated[ str | None,Query(max_length=50)] = None 
    ):
    filtered_data = [filter_data for filter_data in item_data if filter_data['status'] == status]
    if description:
        for data in filtered_data:
            data['description'] = description
    return {"content": filtered_data }


@app.post("/login/")
async def login(username: Annotated[str,Form()],password: Annotated[str,Form()]):
    return {"username":username}

@app.post("/files/")
async def create_file(file: Annotated[list[bytes], File()]):
    print(file)
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(files: list[UploadFile] | None = None):
    if not files:
        return {"file": "Not found"}
    else:
        return {"filename": [file.filename for file in files]}

@app.get("/logs/{item_id}")
async def read_item(item_id : str):
    if item_id not in item_data:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"items": item_data[item_id]}

