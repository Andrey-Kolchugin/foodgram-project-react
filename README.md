# Foodgram

## Описание

Проект **Foodgram** собирает пользовательские рецепты.
Функционал проекта включает в себя:
- **Создание и публикация рецептов**
- **Подписки на понравившихся пользователей**
- **Создание списка избранных рецептов**
- **Добавление в корзину и выгрузка ингридиентов в файл**

---



---

## Технологии в проекте
- **Python 3.10**
- **Django Framework**
- **Django Rest Framework**
- **Django Rest Framework Token**
- **Djoser**
- **Docker**

---

## Процедура локального запуска проекта

Клонировать репозиторий и перейти в него в командной строке и перейти в директорию проекта  
```
git clone https://github.com/Andrey-Kolchugin/foodgram-project-react.git
cd infra
```
Переходим в папку infra и создаем в ней файл .env с переменными окружения, необходимыми для работы приложения.
```

```
```
# Пример заполнения .env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=key
``` 
Запускаем docker compose

```
docker-compose up -d
```
Будут созданы и развернуты контейнеры:
frontend - весь фронт проекта
db - база данных,
backend - приложение бэекенда проекта,
nginx - хранение и раздача медиа и статики.

Далее нужно последовательно выполнить команды миграции, создания суперюзера и сбора статики
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
Проект будет доступен по адресу http://localhost/

### Заполнение базы данных
Авторизоваться по адресу http://localhost/admin/, внести записи в базу данных через админку.

### Создание резервной копии
Бекап можно создать командой
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
### Остановка работы
Оставить работы можно командой
```
docker-compose stop
```
Либо использовать нажатие клавишь  Ctrl+C в терминале, из которого запускались контейнеры 

### Последующие запуски
В дальнейшем использовать команду запуска контейнеров
```
docker-compose start 
```
Успехов!
