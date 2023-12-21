# Online Academy
Этот проект включает в себя управление пользователями, курсами и уроками по API.

## Начало работы 🚀

Перед началом убедитесь, что у вас установлено следующее:

    1. Python версии 3.11 или выше
    2. Poetry для управления зависимостями
    3. Postman для тестирования

## 1. Установка приложения 📦

Для установки выполните следующую команду:

```bash
git clone https://github.com/exetch/online_academy.git
```

## 2. Настройка файла .env и переменные окружения:

Для корректной работы приложения, необходимо создать файл `.env` с вашими данными. Вставьте следующие переменные и заполните их значениями:

```makefile
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=mysecretpassword
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=your_email_host_user
EMAIL_HOST_PASSWORD=your_email_host_password
```

## 3. Настройка суперпользователя 👤

Для создания суперпользователя и установки его параметров, пароля и email, отредактируйте файл `users/management/commands/create_superuser.py`.


## 4. Запуск с использованием Docker 🐳

Для запуска проекта с использованием Docker, выполните следующие шаги:

1. **Создание контейнера PostgreSQL**:
   Для создания контейнера для PostgreSQL, вы можете использовать следующую команду:
   ```bash
   docker run --name my-postgres-container -e POSTGRES_PASSWORD=mysecretpassword -d postgres
   ```
   Это создаст контейнер с именем `my-postgres-container` и паролем `mysecretpassword` для пользователя `postgres`.


2. **Создание Docker образа**:
   Создайте Docker образ. Выполните следующую команду:
   ```bash
   docker-compose build
   ```

3. **Запуск контейнеров**:
   После создания образа можно запустить контейнеры с помощью docker-compose. Это запустит все необходимые сервисы, включая веб-приложение, базу данных PostgreSQL и Redis. Выполните следующую команду:
   ```bash
   docker-compose up
   ```
4. **Применение миграций**:
   После запуска контейнеров необходимо применить миграции к базе данных. Для этого выполните следующую команду:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
   Это применит все необходимые миграции к базе данных в контейнере.

5. **Создание суперпользователя**:

Чтобы создать суперпользователя, выполните следующую команду в командной строке:

```bash
docker-compose exec web python manage.py create_superuser
```


