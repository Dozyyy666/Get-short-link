from pydantic import BaseModel
from typing import Optional

#Модель для входящих данных
class LinkCreate(BaseModel):
    long_url: str #Обязательное поле
    custom_code: Optional[str] = None

#Модель для исходящих данных
class LinkResponse(BaseModel):
    short_url: str
    long_url: str
    clicks: int