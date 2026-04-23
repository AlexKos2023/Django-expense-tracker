# Трекер расходов

Веб-приложение на Django для учета доходов и расходов.

## Возможности
- Добавление доходов и расходов.
- Фильтрация по месяцу и году.
- Просмотр статистики и графиков.
- Скачивание данных в CSV.
- Админка для управления записями.

## Технологии
- Python
- Django
- SQLite
- Plotly

## Установка

```bash
git clone <ссылка на репозиторий>
cd <папка проекта>
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Использование
1. Открой сайт в браузере.
2. Добавляй доходы и расходы.
3. Выбирай месяц и год для фильтрации.
4. Скачивай CSV-файл с данными.

## Админка
Админ-панель доступна по адресу `/admin/`.

## Структура проекта
```text
myapi/
├─ api/
├─ myapi/
├─ manage.py
└─ README.md
```
