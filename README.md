# **🐘 PostgreSQL Database**

Этот проект представляет собой полностью автоматизированное окружение для работы с PostgreSQL.

### **Основные сервисы**

1. **PostgreSQL Database** (`db`)
   - Настраивается через переменные окружения
   - Сохраняет данные в volume (`pgdata`)
   - Встроенный healthcheck для контроля готовности

2. **Database Migrations** (`flyway`)
   - Управление структурой БД через миграции

3. **Test Data Generation** (`data_populator`)
   - Генерация реалистичных тестовых данных

4. **Query Analysis** (`analyze_service`)
   - Тестирование производительности запросов
   - Логирование результатов (cost, execution time)

5. **Backup System** (`backup_service`)
   - Регулярное создание резервных копий
