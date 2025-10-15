from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from mongo_client import get_collection  # Импорт клиента MongoDB
from bson.objectid import ObjectId
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Получение коллекции из MongoDB
users_collection = get_collection()

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Добро пожаловать в веб-приложение на FastAPI с MongoDB!"})

# Страница "О проекте"
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "info": "Это веб-приложение на FastAPI с интеграцией MongoDB. Поддерживает CRUD-операции. Разработчик: Grok AI (на основе инструкций)."})

# Страница с пользователями (HTML или JSON)
@app.get("/users")
async def get_users(request: Request = None, format: str = Query(None)):
    users = list(users_collection.find({}, {"_id": 1, "name": 1, "email": 1}))
    for user in users:
        user["_id"] = str(user["_id"])  # Преобразование ObjectId в строку
    if format == "json":
        return JSONResponse(content={"users": users})
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Страница с формой для добавления пользователя (GET для формы, POST для обработки)
@app.get("/add", response_class=HTMLResponse)
async def add_form(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.post("/add", response_class=HTMLResponse)
async def add_user(request: Request, name: str = Form(...), email: str = Form(...)):
    if users_collection.find_one({"email": email}):
        return HTMLResponse(content="<h1>Ошибка: Email уже существует!</h1>", status_code=400)
    users_collection.insert_one({"name": name, "email": email})
    return templates.TemplateResponse("add.html", {"request": request, "message": f"Пользователь добавлен: {name} ({email})"})

# Страница с формой для удаления пользователя (GET для формы, POST для обработки)
@app.get("/delete", response_class=HTMLResponse)
async def delete_form(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

@app.post("/delete", response_class=HTMLResponse)
async def delete_user(request: Request, user_id: str = Form(...)):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return HTMLResponse(content="<h1>Ошибка: Пользователь не найден!</h1>", status_code=404)
    return templates.TemplateResponse("delete.html", {"request": request, "message": f"Пользователь с ID {user_id} удален."})