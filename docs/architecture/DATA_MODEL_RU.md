# Данные BuildMart (учебный демо-срез)

Полная целевая модель интернет-магазина: users, categories, products, orders, order_items, deliveries, inventory.

Демонстрационный срез намеренно ограничен таблицей `products`:

- V001: `id` PK, `sku` UNIQUE NOT NULL, `name` NOT NULL, `price_rub` NOT NULL.
- V002 (US-102): `unit TEXT` с переводом исторических товаров из тестового набора.
- Применение миграций: по порядку V001 -> V002; `schema_migrations` хранит применённые номера.
- База SQLite для demo. Для production в регламенте предусматривается PostgreSQL, Flyway/Alembic и отдельная процедура миграции.
- Упрощение: V002 в SQLite не добавляет ограничение NOT NULL; проверяется заполненность конкретных исторических SKU. В боевой версии перед требованием NOT NULL нужен отдельный проверенный шаг backfill + constraint.
