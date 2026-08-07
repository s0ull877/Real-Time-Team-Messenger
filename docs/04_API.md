# API Specification

Версия: 1.0

Дата: 03.08.2026

---

# 1. Общая информация

Все HTTP-запросы используют формат JSON.

Базовый URL:

```
/api/v1
```

Все ответы сервера возвращаются в формате JSON.

---

# 2. Аутентификация

Для доступа к защищённым ресурсам используется JWT.

Access Token передаётся в HTTP-заголовке.

```
Authorization: Bearer <access_token>
```

Refresh Token используется только для получения новой пары токенов.

---

# 3. Коды ответов

| Код | Описание |
|------|----------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# 4. Формат ошибок

Все ошибки имеют единый формат.

```json
{
    "detail": "User not found"
}
```

---

# 5. Auth API

## Регистрация

### POST

```
/auth/register
```

### Request

```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "Password123"
}
```

### Response

```json
{
    "id": "uuid",
    "username": "john",
    "email": "john@example.com"
}
```

### Возможные ошибки

- Email already exists
- Username already exists
- Validation Error

---

## Авторизация

### POST

```
/auth/login
```

### Request

```json
{
    "email": "john@example.com",
    "password": "Password123"
}
```

### Response

```json
{
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "Bearer"
}
```

---

## Обновление Access Token

### POST

```
/auth/refresh
```

### Request

```json
{
    "refresh_token": "..."
}
```

### Response

```json
{
    "access_token": "...",
    "refresh_token": "..."
}
```

---

## Выход

### POST

```
/auth/logout
```

Требуется авторизация.

---

# 6. User API

## Получить профиль

### GET

```
/users/me
```

---

## Обновить профиль

### PATCH

```
/users/me
```

---

## Изменить пароль

### PATCH

```
/users/password
```

---

# 7. Room API

## Создать комнату

### POST

```
/rooms
```

---

## Получить список комнат

### GET

```
/rooms
```

---

## Получить комнату

### GET

```
/rooms/{room_id}
```

---

## Добавить участника

### POST

```
/rooms/{room_id}/members
```

---

## Удалить участника

### DELETE

```
/rooms/{room_id}/members/{user_id}
```

---

## Удалить комнату

### DELETE

```
/rooms/{room_id}
```

---

# 8. Message API

## Отправить сообщение

### POST

```
/messages
```

---

## Получить историю комнаты

### GET

```
/rooms/{room_id}/messages
```

Параметры:

| Параметр | Тип |
|-----------|------|
| page | int |
| size | int |

---

## Редактировать сообщение

### PATCH

```
/messages/{message_id}
```

---

## Удалить сообщение

### DELETE

```
/messages/{message_id}
```

Используется Soft Delete.

---

# 9. WebSocket API

Подключение

```
ws://localhost:8000/api/v1/ws
```

JWT передаётся в Query Parameters.

```
ws://localhost:8000/api/v1/ws?token=<JWT>
```

После подключения пользователь получает события в реальном времени.

---

# 10. События WebSocket

## Новое сообщение

```json
{
    "event": "message_created",
    "data": {
        ...
    }
}
```

---

## Изменение сообщения

```json
{
    "event": "message_updated",
    "data": {
        ...
    }
}
```

---

## Удаление сообщения

```json
{
    "event": "message_deleted",
    "data": {
        ...
    }
}
```

---

# 11. Версионирование

Все маршруты API имеют префикс

```
/api/v1
```

При несовместимых изменениях будет использоваться новая версия API.

Например:

```
/api/v2
```