# План тестирования US-102

**Цель:** контроль корректности единиц измерения и миграции каталога.
**Среды:** локальная временная SQLite БД (auto), staging/demo API (manual).
**Состав:** API tests, migration tests, ручной TC-102, smoke test после deployment.
**Подготовка:** применить миграции V001 и V002; проверить SKU CEMENT-M500 и SAND.
**Критерий допуска к release:** автоматические тесты успешны; manual TC-102 Pass; открытых Critical/Blocker нет.
**Отчёт:** JUnit из pytest, Pipeline Test Results и запись ручной проверки.
