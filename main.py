from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
 
from . import crud,models,schema
from .database import SessionLocal, engine
 
models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
#Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
 
@app.post("/users/", response_model=schema.User)
def post_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
 
@app.get("/users/", response_model=list[schema.User])
def get_users(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
 
@app.get("/users/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
 
@app.post("/users/{user_id}/todos/", response_model=schema.Todo)
def post_todo_for_user(user_id: int, todo: schema.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)
 
@app.get("/todos/", response_model=list[schema.Todo])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos