# testcase-kefir

## Описание
Приложение создано для прохождения тестового задания<br>
на роль разработчика в компании "Kefir".<br>
Технологии и стэк используемые в проекте: 
* FastAPI
* PostgresSQL
* Alembic
* SQLAlchemy
* Docker
* passlib

Линтеры и форматтеры: **black, flake8**

## Запуск и проверка проекта

1. Загрузить репозиторий из GitHub:<br>
<code>git clone https://github.com/Kur-up/testcase-kefir.git </code><br><br>
2. Перейти в папку с проектом:<br>
<code>cd testcase-kefir</code><br><br>
3. Запустить приложение (Необходим Docker):<br>
<code>docker compose up -d</code><br><br>
4. Интерфейс Swagger доступен по сслыке:<br>
<code>http://0.0.0.0:8000/docs </code><br><br>
5. Данные для авторизации супер-пользователя:<br>
<code>login: admin</code><br>
<code>password: admin</code><br><br>
6. Остановить приложение:<br>
<code>docker compose down</code><br><br>
7. Удаление созданного образа:<br>
<code>docker rmi testcase-kefir-app</code><br><br>

## Список изменений:

* Логином для авториризации пользователя будет считаться _"email"_<br>
  * Меньше хранимых данных для каждого пользователя<br>
  * Более простое запоминание для пользователя<br>
  * Процедура восстановления пароля будет значительно легче<br><br>

* Пропущено описание ответа 400 (Bad Request) для некоторых конечных точек
  * FastAPI сам валидирует входные данные и создаёт сообщение об ошибке<br><br>
* Из модели _PrivateUpdateUserModel_ удалено поле _id_
  * Нет необходимости передавать идентификатор пользователя, он берётся из параметра пути
<br><br>
* Добавлено корректное описание для всех конечных точкек<br><br>

* Добавлены примеры ответа на запрос для всех конечных точек<br><br>

## Необходимо реализовать:

* Усложнить генерацию временного токена для cookies и ограничить его по времени
<br><br>
* Проставить ограничения на постраничное получение данных о пользователях<br>
  * При больших запросах данных БД может долго отвечать на запрос
  * Это ограничит нагрузку на базу данных
<br><br>
* Добавить volume в docker-compose<br>
  * Для сохранения и переноса данных между запусками приложения

## Разработчик
Lev Kurapov<br>
kurup.performance@gmail.com