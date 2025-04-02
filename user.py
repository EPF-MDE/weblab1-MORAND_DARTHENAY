from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    password: str
    gender: str

app = FastAPI()
users_db: List[User] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api.endpoint")
def first_api():
    return {"message": "Hello"}

@app.get("/users")
async def read_all_users():
    #return {"message": "list of Books"}
    all_users = [user for user in users_db]
    return all_users


@app.get("/users/myuser")
async def read_all_users():
    return {"user_name": "My Name"}

@app.get("/users/{dynamic_param}")
async def read_all_users(dynamic_param):
    return {"dynamic_param": dynamic_param}


@app.post("/users/create_user")
async def create_user(new_user: User):
    new_user.id = len(users_db) + 1
    users_db.append(new_user)
    return {"message": "User created successfully", "book": new_user}

@app.put("/users/update_user/{user_id}")
async def update_user(user_id: int, updated_user: User):
    for i,book in enumerate(users_db):
        if user.id == user_id:
            updated_user.id = user_id
            users_db[i] = updated_user
            return {"message": f"User with id {user_id} has been updated", "user": updated_user}
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

@app.delete("/users/delete_uset/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[i]
            return {"message": f"User with id {user_id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

@app.patch("/users/patch/{user_id}")
async def patch_user(user_id: int, patch_data: User):
    stored_user_data = None
    for user in users_db:
        if user.id == user_id:
            stored_user_data = user
            update_data = patch_data.dict(exclude_unset=True)
            updated_user = stored_user_data.copy(update=update_data)
            users_db[users_db.index(user)] = updated_user
            return {"message": f"User with id {user_id} has been patched", "book": updated_user}
    if stored_user_data is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")