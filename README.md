## Workflow status badge

[![Django-app workflow](https://github.com/jletova/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)](https://github.com/jletova/foodgram-project-react/workflows/foodgram/badge.svg)


Проект Foodgram "Продуктовый помощник" - сайт для любителей кулинарии. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Техонологии:

Проект написан c использованием DRF (Django REST framework), развернут на 3х Docker контейнерах: бекенд, nginx и PostgreSQL. Проект развернут на сайте uletova.com

### Доступ в административную зону:

Проект доступен по адресу: 
```
http://uletova.com/admin
```
Логин: mail@mail.com
Пароль: longpasscode

### Как развернуть проект:

Чтобы развернуть проект локально или на своем сервере необходимо стянуть с гитхаб содежимое папки infra:
```
https://github.com/jletova/foodgram-project-react/tree/master/infra
```
В файл nginx.conf внести изменение: заменить имя сервера на необходимое.

> Для разворачивания контейнеров предварительно должны быть установлены
> [Docker](https://docs.docker.com/get-docker/) и [Docker-compose](https://docs.docker.com/compose/install/)

Для сборки проекта выполните `docker-compose up` в дирректории, где сохранены скаченные файлы.

- Выполнить миграции
```sh
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
```
- Собрать статику
```sh
sudo docker-compose exec -T web python manage.py collectstatic --no-input
```
- Создать суперпользователя
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
- Загрузить ингридиенты для тестирования
```sh
sudo docker-compose exec web python manage.py load_data
```


### Документация:

Подробная документация по API расположена по ссылке:

```
http://uletova.com/api/docs/redoc.html
```
