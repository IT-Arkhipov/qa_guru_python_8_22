## Запуск тестов в различном окружении

### Подготовка для запуска, создание окружения
```
python -m venv .venv
Linux: source .venv/bin/activate
Windows: .venv\Script\activate
pip install poetry
poetry install
pytest .
```

### Browserstack (по умолчанию, можно опустить)
`pytest . --context=bstack`

### Эмулятор Android устройства
`pytest . --context=local_emulator`

### Xiaomi Mi A2
`pytest . --context=local_real`

### Открыти отчетов Allure (если установлен фреймворк)
`allure serve ./allure-results`