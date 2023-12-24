## Запуск тестов в различном окружении

### Browserstack (по умолчанию, можно опустить)
`pytest . --context=bstack`

### Эмулятор Android устройства
`pytest . --context=local_emulator`

### Xiaomi Mi A2
`pytest . --context=local_real`