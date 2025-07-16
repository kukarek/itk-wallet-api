# Wallet API

API-приложение для управления кошельками пользователей с авторизацией через JWT.

---

## Описание

Приложение предоставляет REST API для:

- Регистрации пользователей  
- Авторизации и получения JWT-токена  
- Управления кошельками (просмотр баланса, пополнение, снятие средств)  
- Безопасная работа через аутентификацию JWT

---

## Технологии

- Python 3.11  
- FastAPI  
- PostgreSQL  
- SQLAlchemy (async)  
- Alembic (миграции)  
- JWT (python-jose)  
- Docker и Docker Compose

---


##  Запуск и проверка API

### 1. Клонировать репозиторий

```bash
git clone https://github.com/kukarek/itk-wallet-api.git
cd itk-wallet-api
```

---

### 2. Запустить контейнеры

```bash
docker-compose up --build
```

### 3. Перейти в Swagger UI

Открой в браузере:

```
http://localhost:8000/docs
```

---

### 4. Создать пользователя

В Swagger (`/api/v1/auth/register`) отправь:

```json
{
  "username": "admin",
  "password": "admin1234"
}
```

---

### 5. Авторизуйся в панели Swagger по логину и паролю

### 6. Получить ID своего кошелька

Через sql запрос в отдельном терминале

---
docker exec -it itk-wallet-api-db-1 psql -U postgres 
-d postgres
---

--- sql 
SELECT w.id
FROM wallets w
JOIN users u ON w.user_id = u.id
WHERE u.username = 'admin';
---

## Теперь можно работать с кошельком!