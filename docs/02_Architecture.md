# Architecture

Версия: 1.0

Дата: 03.08.2026

---

# 1. Общая архитектура системы

Real-Time Team Messenger состоит из следующих компонентов:

- Frontend клиент
- Backend API
- PostgreSQL
- Kafka
- SMTP
- Redis
- Docker инфраструктура


Общая схема:

    User Browser

          |
          |
          v

    React + Ant Design

          |
          |
          | HTTP / WebSocket
          |
          v

    FastAPI Backend

          |
    ---------------------
    |          |        |
    v          v        v

 PostgreSQL  Kafka   Redis

                |
                v

            Consumers

                |
                v

              SMTP


---

