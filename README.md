# Hw-2 - Обработка HTTP запросов


## Локальный запуск
1. `python -m venv venv`
2. `source venv/bin/activate` (или `venv\Scripts\activate` на Win)
3. `pip install -r requirements.txt`
4. `python manage.py runserver`

## Запуск через Docker
`docker compose up --build`

## Создание суперпользователя
Админка доступна по адресу /admin/. Для входа нужно создать суперпользователя командой:
`python manage.py createsuperuser`

## Заполнение базы данных
Для заполнения базы данных используйте команду:
`python manage.py fill_db ratio`
Аргумент `ratio` задает коэффициент заполнение:
 - Пользователей - ratio
 - Вопросов - ratio * 10
 - Ответов - ratio * 100
 - Тегов - ratio
