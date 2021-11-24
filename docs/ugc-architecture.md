```plantuml
@startuml
skinparam componentStyle uml2
skinparam sequenceArrowThickness 2
skinparam roundcorner 5
skinparam maxmessagesize 120
skinparam sequenceParticipant underline
hide footbox
skinparam BoxPadding 2

box "Async API" #LightYellow
    actor Client
    collections nginx_async
    collections async_api
end box

box "Auth" #LightBlue
    collections nginx_auth
    collections auth
    database Redis
    database PostgresAuth
end box

box "Transport" #LightGray
    control Kafka
end box

box "UGC" #Orange
    collections ugc
    database Clickhouse
end box

Client -> nginx_async: Event
activate nginx_async
nginx_async -> async_api: Proxy request to backend
activate async_api

alt if auth required and not valid token / missing token
    async_api -> nginx_auth: Redirect /login
    nginx_auth -> auth: Proxy Request
    auth -> Redis: Check if not blacklisted
    Redis -> auth: OK/Forbidden
    auth -> nginx_auth: OK/Forbidden
    nginx_auth -> async_api: OK/Forbidden
else
    async_api -> Kafka: Publish event
end
async_api --> nginx_async: Response/Error
deactivate async_api
Kafka -> ugc

ugc -> Clickhouse: Save event
activate Clickhouse

alt if event saved
    Clickhouse -> ugc: OK
else
    Clickhouse -> ugc: Error
end
deactivate Clickhouse

nginx_async --> Client: Response/Error
deactivate nginx_async
@enduml
```
