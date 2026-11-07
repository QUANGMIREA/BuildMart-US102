# Traceability: US-102 «Единица измерения товара»

| Этап | Артефакт | Состояние на момент выдачи набора |
|---|---|---|
| Требование | US-102 (см. `docs/requirements/US-102_RU.md`) | Локальная спецификация готова; Work Item Azure создавать вручную |
| Задачи | DEV-102-A, DEV-102-B, QA-102-A, QA-102-M | Заданы как шаблон; IDs Azure будут другими |
| Ветка | `feature/US-102-product-unit` | Создана в предоставленном Git-репозитории |
| Исходный код | `app/main.py` | Изменён в feature branch |
| Миграция | `V002__add_product_unit.sql` | Добавлена в feature branch |
| Unit/Integration Tests | `tests/test_api.py`, `tests/test_migrations.py` | Проверить локально перед отправкой |
| Ручной тест | `docs/testing/TC-102_RU.md` | Шаги подготовлены, результат заполняется после исполнения |
| PR -> develop | Azure Repos Pull Request | Ещё не создан; нужен аккаунт Azure DevOps |
| Проверка CI | Azure Pipelines Run + Build Validation | Запускается в Azure после загрузки веток |
| Release | `release/1.0.0`, tag `v1.0.0` | Создать только после одобрения PR и тестирования релиза |
| Deployment | контейнер + Deployment Record | Сделать после создания build artifact |

**Нельзя отмечать незапущенный Azure Pipeline как успешный или приписывать несуществующие Azure Work Item ID.**
