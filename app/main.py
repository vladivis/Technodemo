from fastapi import FastAPI
from .database import Base, engine
from .routes import router

app = FastAPI()

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)

# Регистрация роутов
app.include_router(router)
