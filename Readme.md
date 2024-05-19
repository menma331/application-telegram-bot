# Телеграм бот "Заявки на разработку Ботов"

### 📃 Содержание

1. ✏️ [Описание проекта](#project_desc)
    - 📋 [Задачи](#goals)
    - 📟 [Функциональные возможности](#func_abilities)
2. 📱 [Технологии проекта](#project_technologies)
3. 🔌 [Установка и запуск](#installation_and_launch)
4. 🧙[Авторы](#authors)
   <a name="project_desc"></a>

## ✏️ Описание проекта ##

Этот проект разработан c использованием <a href="https://github.com/aiogram/aiogram">Aiogram</a> с целью показать
результат выполнения тестового задания.

<a name="goals"></a>

### 📋 Задачи ###

<ul>
   <li>✅Добавить меню со следующими кнопками
      <ul>
         <li>Оставить заявку</li>
         <li>Купить товар</li>
         <li>Мой баланс</li>
         <li>Отправить сообщение пользователям</li>
      </ul>
   </li>
   <li>✅Пополнение баланса</li>
   <li>✅Проверка баланса</li>
   <li>✅Рассылка (если администратор)</li>

</ul>
<a name="func_abilities"></a>

### 📟 Функциональные возможности ###

- Регистрация пользователя.
- Заполнить заявку на разработку бота на различных платформах
- Покупка условных единиц
- Пополнение баланса
- Проверка баланса
- Рассылка сообщений пользователям

<a name="project_technologies"></a>

## 📱 Технологии проекта ##

- Язык программирования - `Python`
- База данных - `PosgreSQL`, `SQLAlchemy`
- Фреймворк - `Aiogram 3`

<a name="installation_and_launch"></a>

## 🔌 Установка и запуск ##

1. Скачайте репозиторий. Для сначала создайте новый проект, а затем пропишите в терминале:
   ```commandline
   git clone git@github.com:menma331/order-telegram-bot.git
   ```
2. Создайте виртуальное окружение, а затем пропишите в терминале следующую команду:
   ```commandline
   pip install -r requirements.txt
   ```
3. В корневой директории создайте файл ```.env```. Получите токен бота(
   подробно о том как его получить почитайте <a href="https://www.cossa.ru/instahero/321374/">здесь</a>), а также токен
   youkassa(подробно о том, как получить этот токен, читайте <a href="https://habr.com/ru/companies/selectel/articles/729856/">здесь</a>).

   Затем заполните файл `.env` по примеру ```.env.example```. Должно получиться что то такое:
   ```commandline
   # Database
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_NAME=database_name
   DB_PASS=password_of_database
   
   # Telegram bot API key
   TOKEN=123456789000:AAEmer8CV4dGnGPpEk8Loc0ab7k5e1GEmjA
   
   # Youkassa API key
   YOUKASSA=123456789:TEST:12345
   
   TOKEN=123456789000:AAEmer8CV4dGnGPpEk8Loc0ab7k5e1GEmjA
   
   # Admins id
   admin_id=716775112
   ```
4. После этого,в терминале пропишите команду для миграции:
   ```commandline
   alembic revision --autogenerate
   ```
   а после:
   ```commandline
   alembic upgrade head
   ```

5. Далее через терминал перейдите в папку с проектом(на Windows это можно сделать через cd путь)
   и пропишите
   ```commandline
   python main.py
   ```

<a name="authors"></a>

## 🧙‍️ Авторы

- [Сыса Роман Алексеевич](https://github.com/menma331)
