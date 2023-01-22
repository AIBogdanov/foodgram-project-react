
Описание проекта:
Проект Foodgram позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект запущен по адресу http://51.250.10.2/.
Для ревью:
User: Admin
Password: Admin
e-mail: a@a.com

Документация по API: http://51.250.10.2/api/docs/redoc.

Как запустить проект локально в docker-контейнерах:
Клонировать репозиторий и перейти в него в командной строке:

git@github.com:AIBogdanov/foodgram-project-react.git
cd foodgram-project-react


Что бы не было ошибки безопастности добавляем используемые хосты в переменную:
CSRF_TRUSTED_ORIGINS = ['http://localhost:81', 'http://127.0.0.1:81'] 

Перейти в папку backend и подготовить файл переменных окружения .env:
'DB_ENGINE', default='django.db.backends.postgresql',
'DB_NAME', default='postgres',
'POSTGRES_USER', default='postgres',
'POSTGRES_PASSWORD', default='postgres',
'DB_HOST', default='db',
'DB_PORT', default='5432'
Перейти в папку развёртывания инфраструктуры:

cd ../infra
Запустить приложение в docker-контейнерах:

docker-compose up -d
Выполнить миграции и сбор статики:

docker-compose exec web python3 manage.py migrate
docker-compose exec web python3 manage.py collectstatic --no-input
Теперь проект доступен по адресу http://127.0.0.1/,
документация по API проекта - по адресу http://127.0.0.1/api/docs/redoc.

Заполнить данными таблицу ингредиентов можно командами:

Создать суперпользователя
docker-compose exec web python3 manage.py createsuperuser
Теперь по адресу http://127.0.0.1/admin/ доступна админка проекта.

