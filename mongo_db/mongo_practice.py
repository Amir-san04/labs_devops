from pymongo import MongoClient

# 1️⃣ Подключение к локальному серверу MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 2️⃣ Подключение к существующей базе и коллекции
db = client["people_database"]
collection = db["users"]

# 3️⃣ Проверяем, какие документы уже есть
print("📋 Текущие записи в коллекции users:")
for user in collection.find():
    print(user)

# 4️⃣ Ищем конкретного пользователя по имени (пример: Иван)
print("\n🔍 Поиск пользователя с именем 'Иван':")
user = collection.find_one({"first_name": "Иван"})
if user:
    print("Найден:", user)
else:
    print("Пользователь с именем 'Иван' не найден.")

# 5️⃣ Если найден — обновим его email
if user:
    new_email = "ivan.petrov@newmail.com"
    update_result = collection.update_one(
        {"first_name": "Иван"},                  # фильтр
        {"$set": {"email": new_email}}           # новые данные
    )
    if update_result.modified_count > 0:
        print(f"\n✅ Email пользователя 'Иван' изменён на {new_email}")
    else:
        print("\n⚠️ Данные уже были актуальными — изменений нет.")

# 6️⃣ Проверим обновлённые данные
print("\n📄 Данные после обновления:")
for user in collection.find():
    print(user)
