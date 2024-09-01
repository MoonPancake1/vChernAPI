# vC.ID && vC.Main API v.0.1.0.3
Автор: Чернышев Владислав

## О проекте:
Создан для поддержки других проектов. Единый API 
для всех продуктов, которые могут быть интегрированы
в эту сеть. Удобный доступ с единого аккаунта в
разные проекты и системы

## Для запуска:
1. Склонировать репозиторий
2. Создать виртуальное окружение командой: ```python3 -m venv *название окружения*```
3. Установить все зависимости: ```pip install -r requirements.txt```
4. Создать в папке проекта файл .env и .env.db
5. Добавить следующие переменные в .env:
```
# Project Settings
PROJECT_NAME
DEBUG
VERSION
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS

# DB Settings
DB_ENGINE
DB_USER
DB_PASSWORD
DB_HOST
TEST_DB_HOST
DB_NAME

# API Settings
API_URL

# Telegram OAuth2
PROD_TELEGRAM_BOT_TOKEN
DEVELOP_TELEGRAM_BOT_TOKEN

# VK.ID OAuth2
VK_ID_CLIENT
```
6. Добавить следующие переменные в .env.db:
```
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
TEST_POSTGRES_USER
TEST_POSTGRES_PASSWORD
```
7. Запустить проект командой: ```uvicorn main:app --reload```
8. Создать миграцию: ```alembic revision --autogenerate -m "Name revision"```
9. Произвести миграцию: ```alembic upgrade (REVISION | head)```


## Обновления:

- vC.ID && vC.Main API **v.0.1.0.3**:
Фикс отображения кнопки VK.ID

- vC.ID && vC.Main API **v.0.1.0.2**:
Добавление авторизации с помощью VK.ID

- vC.ID && vC.Main API **v.0.1.0.1**:
Обновлён стиль страницы авторизации

- vC.ID && vC.Main API **v.0.1.0.0**:
Первое глобальное обновление. Добавлена
авторизация и регистрация с помощью 
аккаунта в telegram

- vC.ID && vC.Main API **v.0.0.4.14**:
Обновлён README, добавлен новый endpoint 
для создания пользователя через telegram

- vC.ID && vC.Main API **v.0.0.4.13**:
Добавлен новый endpoint /id/login/ и
тестирование авторизации через telegram

- vC.ID && vC.Main API **v.0.0.4.12**:
Изменена CORS политика для тестирования
загрузки изображений

- vC.ID && vC.Main API **v.0.0.4.11**:
Обновлена система хранения статических 
изображений

- vC.ID && vC.Main API **v.0.0.4.10**:
Обновлён endpoint для vC.ID id/get/.
Теперь выдаётся базовая информация о пользователе

- vC.ID && vC.Main API **v.0.0.4.9**:
Обновлён endpoint для vC.ID id/get/.
Теперь необходимо передавать не id пользователя,
а его uuid

- vC.ID && vC.Main API **v.0.0.4.8**:
Фикс мелких багов. Добавлен новый endpoint
для получения всех технологий, которые
используются во всех проектах

- vC.ID && vC.Main API **v.0.0.4.7**:
Добавлен функционал к оценкам проектов.
Исправлена ошибка при выдачи ошибки с кодом 200, 
на код ошибки

- vC.ID && vC.Main API **v.0.0.4.6**:
Исправлена ошибка с выдачей комментариев к
посту

- vC.ID && vC.Main API **v.0.0.4.5**:
добавлен функционал для работы с достижениями.
Переработана выдача ошибочных запросов

- vC.ID && vC.Main API **v.0.0.4.4**:
добавлен функционал для работы с комментариями 
пользователей. Добавлена дополнительная проверка
для добавления оценки на проект

- vC.ID && vC.Main API **v.0.0.4.3**: обновлена 
защита базы данных и создана новая база данных
для тестирования функционала для разработки.
Появилась возможность работать с оценками для
проектов

- vC.ID && vC.Main API **v.0.0.4.2**: для сервиса vC.Main
был переработан способ аунтефикации пользователей
по ключу

- vC.ID && vC.Main API **v.0.0.4.1**: доработана логика
для работы с проектами, обновление структуры бд

- vC.ID && vC.Main API **v.0.0.4.0**: обновлена
структура приложения для добавления ещё одного
сервиса, реализована возможность добавления
проекта

- vC.ID API **v.0.0.3.2**: добавлена возможность
создавать и производить миграции в приложении

- vC.ID API **v.0.0.3.1**: исправлена ошибка 
проверки bearer token, рефакторинг кода

- vC.ID API **v.0.0.3.0**: обновление выпуска 
access токенов; добавлена возможность выпуска 
refresh токенов; обновлена возможность проверки
пользователей для регистрации или редактирования
информации о пользователе

- vChernAPI **v.0.0.2.7**: обновление Dockerfile

- vChernAPI **v.0.0.2.6**: обновление предеардресации
для openapi.json

- vChernAPI **v.0.0.2.5**: срочное исправление url 
для nginx

- vChernAPI **v.0.0.2.4**: исправление ошибок связанных
с docker-compose и тестовая равзвёртка на севрере

- vChernAPI **v.0.0.2.3**: добавление docker-compose

- vChernAPI **v.0.0.2.2**: небольшой рефакторинг кода

- vChernAPI **v.0.0.2.1**: обновил движок базы данных
доработал Dockerfile

- vChernAPI **v.0.0.2.0**: доступно развёртываение
проекта с помощью docker, а так же добавлена возможность
выдачи статического контента

- vChernAPI **v.0.0.1.5**: переработан файл с 
переменными окружения и добавлен гайд по
установке приложения в файл _**README.md**_

- vChernAPI **v.0.0.1.4**: добавлена возможность
проверки пользователя на администратора и оптимизирована
работа приложения

- vChernAPI **v.0.0.1.3**: обновление модели
пользователя и рефакторинг кода

- vChernAPI **v.0.0.1.2**: обновление системы
аунтефикации пользователей

- vChernAPI **v.0.0.1.1**: оформление кода и 
стилизация для удобства чтения

- vChernAPI **v.0.0.1.0**: структуризация проекта
добавление авторизации по nickname и password

- vChernAPI **v.0.0.0.2**: добавление проверки на 
авторизацию пользователя и улучшение пользовательской
модели

- vChernAPI **v.0.0.0.1**: создание основных функций 
crud и изучение фреймворка