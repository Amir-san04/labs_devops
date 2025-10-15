from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from typing import List

app = FastAPI()

# Получаем URL MongoDB из окружения или локальный
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URL)

# Проверяем соединение
try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except ConnectionFailure:
    print("MongoDB connection failed")

db = client["testdb"]
collection = db["users"]

# Модель для пользователя
class User(BaseModel):
    name: str
    email: str
    age: int

# GET: главная
@app.get("/")
async def root():
    return {"message": "FastAPI app is running"}

# GET: все пользователи
@app.get("/users/", response_model=List[User])
async def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return users

# POST: добавить пользователя (JSON body)
@app.post("/users/", response_model=User)
async def create_user(user: User):
    result = collection.insert_one(user.dict())
    if result.inserted_id:
        return user
    raise HTTPException(status_code=500, detail="Failed to create user")

# DELETE: удалить по email
@app.delete("/users/{email}")
async def delete_user(email: str):
    result = collection.delete_one({"email": email})
    if result.deleted_count > 0:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")