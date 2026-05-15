# Happy Day — дневник силы

MVP Telegram-бота для ежедневного дневника успеха, благодарности и мягкой персональной поддержки.

## Что умеет

- `/start` — знакомство, имя и стиль общения.
- `/diary` — вечерний дневниковый сценарий.
- AI-ответ через OpenRouter OpenAI-compatible API.
- `/history` — последние 5 записей.
- `/week` — бережный итог недели.
- `/help` — короткая подсказка по командам.
- Ежедневное напоминание в 21:00.
- Антикризисный ответ на фразы вроде `я устала`, `я плохая`, `всё плохо`.

## Локальный запуск

1. Перейдите в папку проекта:

```bash
cd happy_day_bot
```

2. Создайте виртуальное окружение:

```bash
python -m venv .venv
```

3. Активируйте окружение.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Установите зависимости:

```bash
pip install -r requirements.txt
```

5. Создайте `.env` рядом с `.env.example`:

```env
BOT_TOKEN=ваш_токен_telegram_бота
OPENROUTER_API_KEY=ваш_ключ_openrouter
OPENROUTER_MODEL=openrouter/free
DATABASE_PATH=happy_day.sqlite3
TIMEZONE=Europe/Moscow
```

По умолчанию используется официальный бесплатный роутер OpenRouter `openrouter/free`. Его можно заменить на любую доступную модель с суффиксом `:free`.

6. Запустите бота:

```bash
python main.py
```

## Структура

```text
happy_day_bot/
  main.py
  config.py
  database.py
  handlers/
    start.py
    diary.py
    history.py
    week.py
  services/
    ai.py
    reminders.py
  keyboards.py
  states.py
  requirements.txt
  .env.example
  README.md
```
