# Database Design

Версия: 1.0

Дата: 03.08.2026

---

# 1. Общая информация

В качестве основной базы данных используется **PostgreSQL**.

Доступ к базе данных осуществляется посредством **SQLAlchemy 2.x** в асинхронном режиме.

Все изменения структуры базы данных выполняются исключительно через **Alembic**.

---

# 2. Основные принципы

При проектировании базы данных используются следующие правила:

- все сущности имеют первичный ключ `UUID`;
- все даты хранятся в формате `TIMESTAMP WITH TIME ZONE`;
- связи между сущностями реализуются посредством `FOREIGN KEY`;
- удаление сообщений выполняется посредством **Soft Delete**;
- изменение структуры базы данных осуществляется только через миграции Alembic.

---

# 3. Сущности

В рамках первой версии проекта используются следующие сущности:

- User
- Room
- RoomMember
- Message
- RefreshToken

---

# 4. Таблица User

Назначение:

Хранение информации о зарегистрированных пользователях.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK | Идентификатор пользователя |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Имя пользователя |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email |
| password_hash | VARCHAR | NOT NULL | Хэш пароля |
| avatar_url | VARCHAR | NULL | Ссылка на аватар |
| is_verified | BOOLEAN | DEFAULT FALSE | Подтверждение Email |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Дата регистрации |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Последнее изменение |

---

# 5. Таблица Room

Назначение:

Хранение информации о чат-комнатах.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK | Идентификатор комнаты |
| name | VARCHAR(100) | NOT NULL | Название комнаты |
| owner_id | UUID | FK(User.id) | Создатель комнаты |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Дата создания |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Последнее изменение |

---

# 6. Таблица RoomMember

Назначение:

Связующая таблица между пользователями и комнатами.

Один пользователь может состоять во многих комнатах.

Одна комната может содержать множество пользователей.

Тип связи:

**Many-to-Many**

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| room_id | UUID | PK, FK(Room.id) | Комната |
| user_id | UUID | PK, FK(User.id) | Пользователь |
| joined_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Дата вступления |

---

# 7. Таблица Message

Назначение:

Хранение сообщений пользователей.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK | Идентификатор сообщения |
| room_id | UUID | FK(Room.id) | Комната |
| author_id | UUID | FK(User.id) | Автор |
| text | TEXT | NOT NULL | Текст сообщения |
| edited_at | TIMESTAMP WITH TIME ZONE | NULL | Дата изменения |
| deleted_at | TIMESTAMP WITH TIME ZONE | NULL | Soft Delete |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Дата создания |

Сообщения не удаляются физически.

При удалении устанавливается значение поля `deleted_at`.

---

# 8. Таблица RefreshToken

Назначение:

Хранение Refresh JWT токенов.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK | Идентификатор |
| user_id | UUID | FK(User.id) | Пользователь |
| token_hash | VARCHAR(64) | UNIQUE, NOT NULL | SHA-256 хэш Refresh Token |
| expires_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Срок действия |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL | Дата создания |

---

# 9. Связи между сущностями

```
User
 │
 ├──────────────┐
 │              │
 ▼              ▼
Room        RefreshToken
 │
 ▼
RoomMember
 ▲
 │
User

Room
 │
 ▼
Message
 ▲
 │
User
```

---

# 10. Индексы

Для повышения производительности создаются следующие индексы:

## User

- email (UNIQUE)
- username (UNIQUE)

## Room

- owner_id

## RoomMember

- room_id
- user_id

## Message

- room_id
- author_id
- created_at

## RefreshToken

- user_id
- expires_at

---

# 11. Ограничения

## User

- Email должен быть уникальным.
- Username должен быть уникальным.

## RoomMember

Не допускается повторное добавление одного пользователя в одну комнату.

Реализуется составным первичным ключом:

```
(room_id, user_id)
```

---

# 12. Правила удаления данных

## User

Удаление пользователя не приводит к удалению сообщений.

Сообщения остаются в истории.

---

## Room

Удаление комнаты приводит к удалению:

- участников комнаты;
- сообщений комнаты.

---

## Message

Используется **Soft Delete**.

Запись не удаляется физически.

Устанавливается значение поля `deleted_at`.

---

# 13. ER-диаграмма

```
                User
          ┌───────────────┐
          │ id            │
          │ username      │
          │ email         │
          └──────┬────────┘
                 │
      ┌──────────┼─────────────┐
      │          │             │
      ▼          ▼             ▼
 Room       RefreshToken    Message
      ▲                      ▲
      │                      │
      └──────RoomMember──────┘
```

---

# 14. План дальнейшего расширения

В следующих версиях проекта планируется добавить:

- Attachments
- Reactions
- Notifications
- Roles
- Read Status
- Pinned Messages
- Private Dialogs
- Message Search