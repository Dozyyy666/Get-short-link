from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.schemas.link import LinkCreate, LinkResponse
from app.crud import link as crud_link
from app.database import get_db_connection

router = APIRouter()

#POST запрос: создание короткой ссылки
@router.post("/shorten", response_model=LinkResponse, status_code=201)
def create_short_link(data: LinkCreate):
    db = get_db_connection() #Подключаемся к БД

    try:
        #Передаем проверенные данные из schemas в функцию CRUD
        result = crud_link.create_link(
            db_conn=db,
            long_url=data.long_url,
            custom_code=data.custom_code,
        )

        #Формируем ответ для пользователя
        return {
            "short_url": f"/go/{result['short_code']}",
            "long_url": result['long_url'],
            "clicks": result['clicks']
        }

    except ValueError as e:
        #Если CRUD выбросил ошибку (код занят), ловим ее и превращаем в HTTP-ответ
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        #Всегда закрывает подключение к БД, даже если произошла ошибка
        db.close()

#GET запрос: перенаправление по короткой ссылке
@router.get("/go/{short_code}")
def redirect_to_url(short_code: str):
    db = get_db_connection()

    try:
        #ищем ссылку в базе
        link_data = crud_link.get_link_by_code(db,short_code)

        #Если не нашли - выдаем стандартную HTTP ошибку 404
        if not link_data:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")

        #Если нашли - увеличиваем счетчик переходов
        crud_link.increment_clicks(db, short_code)

        #Возвращаем редирект, браузер автоматически перейдет по long_url
        return RedirectResponse(url=link_data['long_url'], status_code=307)

    finally:
        db.close()