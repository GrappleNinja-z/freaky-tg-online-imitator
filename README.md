# Telegram Userbot Self-Chat

Автоматический userbot для создания активности в приватной группе Telegram.

## Быстрый старт

### Локально

```bash
# 1. Клонируй
git clone <твой-репо>
cd <твой-репо>

# 2. Создай виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Настрой переменные окружения
cp .env.example .env
# Отредактируй .env своими значениями

# 5. Сгенерируй StringSession (ОДИН РАЗ)
python generate_session.py
# Скопируй полученную строку в .env как TELEGRAM_SESSION

# 6. Запусти
python userbot_self_chat.py
```

### Получение API credentials

1. Иди на https://my.telegram.org/apps
2. Войди со своим номером телефона
3. Создай приложение, получи `API_ID` и `API_HASH`

### Генерация StringSession

StringSession позволяет запускать бота без интерактивного ввода SMS-кода:

```bash
# Заполни .env файл (API_ID, API_HASH, PHONE)
python generate_session.py
```

Скрипт попросит ввести код из Telegram **один раз**, затем выдаст строку сессии.
Эту строку добавь в `.env` как `TELEGRAM_SESSION` и в GitHub Secrets.

### GitHub Secrets

Добавь в **Settings → Secrets and variables → Actions**:

- `TELEGRAM_API_ID` - твой API ID
- `TELEGRAM_API_HASH` - твой API Hash
- `TELEGRAM_SESSION` - строка сессии из `generate_session.py`

⚠️ **НЕ добавляй `TELEGRAM_PHONE` в GitHub Secrets** - он нужен только для генерации сессии локально.

CI запустится автоматически при push в main.

## Безопасность

✅ Секреты только в переменных окружения  
✅ `.env` в `.gitignore`  
✅ GitHub Actions инжектит секреты на CI  
✅ Session работает без интерактивного ввода кода  
✅ Session файлы не коммитятся
