<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

<div align="center">
  <h6 align="center">
    <a href="https://amonitoring.ru/#gh-light-mode-only">
    <img width="20%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/9522302b-bd18-47c8-961d-e1da3cfddd80">
    </a>
    <a href="https://amonitoring.ru/#gh-dark-mode-only">
    <img width="20%" src="https://github.com/advancedmonitoring/hba-boilerplate/assets/15703713/0aad4d95-9a59-45e9-ab92-29cd8708e7a5">
    </a>
  </h6>

# HBA Demo todo app

Данный репозиторий содержит демо приложение основанное на [HBA архитектуре](https://github.com/advancedmonitoring/hba-boilerplate).

[Описание](#описание) •
[Запуск](#запуск)
</div>

## Описание

Данный проект показывает основные возможности HBA архитектуры:
* реализован API интерфейс для взаимодействия
* Ws интерфейс для обновления данных на клиенте
* Несколько Ws групп для демонстрации
* Группа Ws для конкретного объекта
* Swagger документация
* Swagger документация для Ws

Основные сущности проекта: `Note` - блокнот и `Todo` - запись в блокноте. Ролевая модель проста: каждый может 
добавить блокнот и делать записи в нём. Изменять и удалять можно только собственные данные (как блокноты, так и 
записи в них).

## Запуск

Запустить сервер:
* Перейти в каталог `backend`
* Создать виртуальное окружение
* Настроить файл с локальными настройками 
  * Создать файл `config/settings/local.py`
  * Указать нужные локальные настройки
* Применить миграции (`python manage.py migrate`)
* Создать суперпользователя (`python manage.py createsuperuser`)
* Запустить сервер (`python manage.py runserver`)

Запустить frontend сервер:
* Перейти в каталог `frontend`
* Установить зависимости (`npm install`)
* запустить frontend сервер (`npm run serve`)



