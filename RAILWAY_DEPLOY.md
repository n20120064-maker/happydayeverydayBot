# Деплой Happy Day на Railway

Railway будет запускать бота командой:

```bash
python happy_day_bot/main.py
```

## Переменные окружения

В Railway открой сервис → `Variables` → `RAW Editor` и вставь:

```env
BOT_TOKEN=токен_telegram_бота
OPENROUTER_API_KEY=ключ_openrouter
OPENROUTER_MODEL=openrouter/free
DATABASE_PATH=happy_day.sqlite3
TIMEZONE=Europe/Moscow
```

Для более надежного хранения SQLite можно подключить Railway Volume и поставить:

```env
DATABASE_PATH=/data/happy_day.sqlite3
```

## Через сайт Railway

1. Открой https://railway.com/new
2. Выбери `Deploy from GitHub repo`.
3. Подключи репозиторий с этим проектом.
4. После создания сервиса открой `Variables`.
5. Добавь переменные из блока выше.
6. Нажми `Deploy` или `Redeploy`.
7. В логах должно появиться `Run polling for bot @happydayeverydayBot`.

## Важно

На Railway должен быть запущен только один экземпляр Telegram polling-бота.
Когда Railway-деплой заработает, локальный процесс на компьютере лучше остановить, иначе два процесса могут конфликтовать за получение сообщений.
