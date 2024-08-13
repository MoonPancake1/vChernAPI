# vC.ID && vC.Main API v.0.0.4.3
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
4. Создать в папке проекта файл .env
5. Добавить следующие переменные в этот файл:
  - PROJECT_NAME (название проекта)
  - DEBUG (отладка)
  - VERSION (версия приложения)
  - SECRET_KEY (секретный ключ)
  - ALGORITHM (алгоритм шифрования рекомендация:
"HS256")
  - ACCESS_TOKEN_EXPIRE_MINUTES (сколько минут 
будет доступен токен авторизации пользователя)
  - DB_ENGINE (движок базы данных)
  - DB_USER (пользователь базы данных)
  - DB_PASSWORD (пароль пользователя)
  - DB_HOST (хост для подключения)
  - DB_NAME (название базы данных)
  - API_URL (путь до api)
6. Запустить проект командой: ```uvicorn main:app --reload```
7. Создать миграцию: ```alembic revision --autogenerate -m "Name revision"```
8. Произвести миграцию: ```alembic upgrade REVISION```


## Обновления:

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