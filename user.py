from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional

class Users(BaseModel):
    id: Optional[int] = None
    name: str
    username_mail: str
    password: Optional[str] = None
    gender: str

app = FastAPI()
user_db: List[Users] = []

@app.get("/users/{dynamic_param}")
async def read_all_user(dynamic_param):
    return {"dynamic_param": dynamic_param}

@app.get("/users")
async def read_all_user():
    all_user = [user for user in user_db]
    return all_user

@app.get("/users/myuser")
async def read_all_user(dynamic_param):
    return {"user_title": "My user"}

@app.post("/users/create_user")
async def create_user(new_user: Users):
    new_user.id = len(user_db) + 1 
    user_db.append(new_user)
    return {"message": "user have been created successfully", "user": new_user}

@app.put("/users/update_user/{user_id}")
async def update_user(user_id: int, updated_user: Users):
    for i, user, in enumerate(user_db):
        if user.id == user_id:
            updated_user.id = user_id
            user_db[i] = updated_user
            return {"message": f"User with id {user_id} has been updated", "user": updated_user}
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
@app.delete("/users/delete_user/{user_id}")
async def delete_user(user_id: int):
    for i, user, in enumerate(user_db):
        if user.id == user_id:
            del user_db[i]
            return {"message": f"User with id {user_id} has been delated"}
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
@app.patch("/users/patch/{user_id}")
async def patch_user(user_id: int, patch_data: Users):
    stored_user_data = None
    for user in user_db:
        if user.id == user_id:
            stored_user_data = user
            update_data = patch_data.dict(exclude_unset=True)
            updated_user = stored_user_data.copy(update=update_data)
            user_db[user_db.index(user)] = updated_user
            return {"message": f"User with id {user_id} has been patched", "user": updated_user}
    if stored_user_data is None:
        raise HTTPException(status_code = 404, detail = f"User with id {user_id} not found")