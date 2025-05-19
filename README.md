# Django Barter Platform API

API для платформы обмена вещами между пользователями. Позволяет создавать объявления, управлять предложениями обмена и взаимодействовать с другими пользователями.

## Технический стек

- Python 3.9+
- PostgreSQL
- Django 4.2+
- DRF (Django REST Framework)
- Django Templates для создания HTML-страниц

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
## Как пользоваться
Для того чтобы создавать объявления/предложения_обмена с помощью страниц или запросов, нужно создать пользователя:```bash python manage.py createsuperuser ``` 
Или таким образом в python shell user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
После чего перейти на http://localhost:8000/admin/ и войти в аккаунт. 

Также в [Swagger](http://localhost:8000/api/v1/swagger/) есть Basic authorization, с её помощью можно также войти и отправлять запросы на создание/измение и так далее.
## API Endpoints
Базовый URL для REST API: http://localhost:8000/api/v1/

Базовый URL для HTML-страницы: http://localhost:8000/ads/
## Документация API
- Swagger UI: http://localhost:8000/api/v1/swagger/
- ReDoc: http://localhost:8000/api/v1/redoc/

---

## Endpoints для HTML‑страниц и REST API

### HTML‑страницы

| URL                                | Представление (View)            | Название маршрута | Описание                            |
|------------------------------------|---------------------------------|-------------------|-------------------------------------|
| `/ads/`                            | `AdListView`                    | `ads:list`        | Список объявлений                   |
| `/ads/create/`                     | `AdCreateView`                  | `ads:create`      | Создать объявление                  |
| `/ads/<pk>/`                       | `AdDetailView`                  | `ads:detail`      | Детальный просмотр объявления       |
| `/ads/<pk>/edit/`                  | `AdUpdateView`                  | `ads:edit`        | Редактировать объявление            |
| `/ads/<pk>/delete/`                | `AdDeleteView`                  | `ads:delete`      | Удалить объявление                  |
| `/ads/proposals/`                  | `ProposalListView`              | `ads:proposal-list`    | Список предложений обмена           |
| `/ads/proposals/create/`           | `ProposalCreateView`            | `ads:proposal-create`  | Создать предложение обмена          |
| `/ads/proposals/<pk>/`             | `ProposalDetailView`            | `ads:proposal-detail`  | Детальный просмотр предложения      |
| `/ads/proposals/<pk>/edit/`        | `ProposalUpdateView`            | `ads:proposal-edit`    | Редактировать предложение           |
| `/ads/proposals/<pk>/delete/`      | `ProposalDeleteView`            | `ads:proposal-delete`  | Удалить предложение                 |

### REST API (DRF v1)

| URL                                    | Метод | ViewSet / View            | Описание                                  |
|----------------------------------------|-------|---------------------------|-------------------------------------------|
| `/api/v1/ads/`                         | GET   | `AdvertisementViewSet`    | Список объявлений                         |
| `/api/v1/ads/`                         | POST  | `AdvertisementViewSet`    | Создать объявление                        |
| `/api/v1/ads/<pk>/`                    | GET   | `AdvertisementViewSet`    | Детальный просмотр объявления             |
| `/api/v1/ads/<pk>/`                    | PUT   | `AdvertisementViewSet`    | Полное обновление                         |
| `/api/v1/ads/<pk>/`                    | PATCH | `AdvertisementViewSet`    | Частичное обновление                      |
| `/api/v1/ads/<pk>/`                    | DELETE| `AdvertisementViewSet`    | Удалить объявление                        |
| `/api/v1/proposals/`                   | GET   | `ExchangeProposalViewSet` | Список предложений                        |
| `/api/v1/proposals/`                   | POST  | `ExchangeProposalViewSet` | Создать предложение                       |
| `/api/v1/proposals/<pk>/`              | GET   | `ExchangeProposalViewSet` | Детальный просмотр предложения            |
| `/api/v1/proposals/<pk>/`              | PATCH | `ExchangeProposalViewSet` | Изменить статус или комментарий           |
| `/api/v1/proposals/<pk>/`              | DELETE| `ExchangeProposalViewSet` | Удалить предложение                       |

---

