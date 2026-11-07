# Реестр артефактов BuildMart — эталон для пунктов 3–9

Реестр не должен произвольно расширяться в следующих разделах: новый артефакт добавляется сначала сюда и в раздел 3 регламента. Все коды ниже — условные, идентификаторы Azure Boards присваиваются автоматически.

| ID | Артефакт | Кто создаёт / когда | Где хранится и версия | Критерий готовности (DoD) |
|---|---|---|---|---|
| A01 | Vision / требования | BA/PM, инициация и уточнение | `docs/requirements/`, Git | Цели, границы, критерии и одобрение |
| A02 | Epic, Feature, User Story, Product Backlog | PM/BA, планирование | Azure Boards, Work Item ID | Связи, приоритет, исполнитель, критерии приемки |
| A03 | Task, Bug, Issue, Kanban Board | PM/Dev/QA, на протяжении итерации | Azure Boards, Work Item ID | Назначен, статус и результат подтверждены |
| A04 | Архитектура, схема данных, API contract | Tech Lead, проектирование | `docs/architecture/`, Git | Рецензирование и связь с требованиями |
| A05 | Исходный код, feature branch, commit, PR | Developer, реализация | Azure Repos Git, SHA и PR ID | CI зелёный, review, нет блокирующих конфликтов |
| A06 | SQL migrations / схема БД | Developer/DBA, изменение данных | `database/migrations/`, Git | Применяется по порядку, проверена на данных |
| A07 | Test Plan / Test Case / automated test code | QA/Developer, до тестирования | Azure Test Plans или `docs/testing/`, `tests/` | Шаги, ожидаемые результаты, связь с Story |
| A08 | Test Run / Test Report / Test Log | QA и CI, во время тестирования | Pipeline Tests и `docs/testing/` | Фактические результаты, время, версия, вывод |
| A09 | Bug Report / Defect | QA, при обнаружении дефекта | Azure Boards Bug | Шаги, severity, expected/actual, связанный тест |
| A10 | Build artifact / release candidate | CI/DevOps, перед выпуском | Azure Pipelines Artifacts, build ID | Сборка и обязательные тесты пройдены |
| A11 | Release Checklist / Release Notes / Git tag | Release Manager, перед release | `docs/releases/`, Azure Repos | Решение об одобрении, версия и список изменений |
| A12 | Deployment Record / Rollback Plan | DevOps, на развертывании | `docs/releases/` + Pipelines | Среда, результат, откат, ответственное лицо |
| A13 | Operations Runbook / BCP | PM/DevOps, перед pilot | `docs/operations/`, Git | Альтернативный порядок обработки заказов проверен |
| A14 | Регламент + review/история версий | Все участники, каждый цикл | `docs/reglament/`, Git | Проверены пункты 1–9 и 4 практических этапа |
| A15 | Traceability Matrix | BA/QA, при изменении Story | `docs/artifacts/TRACEABILITY_US102_RU.md` | Story -> Task -> code -> migration -> tests -> PR -> release -> deploy |

## Ответственность команды из трёх человек

| Роль | Ответственность |
|---|---|
| PM / BA | A01-A03, приоритеты, приемка, A11, A14-A15 |
| Tech Lead / Developer / DevOps | A04-A06, A10, A12, код и CI |
| QA / Developer | A07-A09, ручные тесты, review чужих PR |

Роли совмещаются, но свой PR автор не подтверждает самостоятельно. В реальном проекте нужен контроль доступа и отдельное утверждение выпуска.

## Связь этапов

`A02 User Story -> A03 Task -> A05 Git + A06 Migration -> A07 Test Cases -> A08 Test Run / A09 Bug -> A10 Build -> A11 Release -> A12 Deployment -> A13 Operations`, а `A15` связывает все элементы.
