# Django Barter Platform API

API для платформы обмена вещами между пользователями. Позволяет создавать объявления, управлять предложениями обмена и взаимодействовать с другими пользователями.

## Технический стек

- Python 3.9+
- PostgreSQL
- Django 4.2+
- DRF (Django REST Framework)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/StudentDaniil/barter_system.git
cd barter_system
```
Установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
2. Настройте базу данных в settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## Миграции
```bash
python manage.py makemigrations models
python manage.py migrate
```
## Запуск сервера
```bash
python manage.py runserver
```
## Тестирование 
```bash
python manage.py test
```
## API Endpoints
Базовый URL endpoints: http://localhost:8000/api/v1/
## Документация API
- Swagger UI: http://localhost:8000/api/v1/swagger/
- ReDoc: http://localhost:8000/api/v1/redoc/
