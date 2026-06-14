# Personal Finance Tracker Bot

Telegram orqali daromad va xarajatlarni yozib borish, kategoriyalar bilan saqlash, oylik statistika va CSV hisobot olish uchun bot.

## Texnologiyalar

- Python 3.11+
- Aiogram 3
- PostgreSQL
- asyncpg
- python-dotenv

## Ishga tushirish

1. Virtual muhit va kutubxonalar:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. PostgreSQL bazani tayyorlash:

```bash
sudo -u postgres psql
CREATE DATABASE finance_bot;
CREATE USER botuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE finance_bot TO botuser;
ALTER DATABASE finance_bot OWNER TO botuser;
\q
```

3. `.env.example` dan `.env` yarating va qiymatlarni to'ldiring:

```bash
BOT_TOKEN=8904508189:AAGPUszGFjmFrM0IE4bnTRCV5H_ir-YXLrg
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finance_bot
DB_USER=botuser
DB_PASS=120012.Shoh
```

4. Botni ishga tushirish:

```bash
python bot.py
```

Bot birinchi `/start` bosilganda til tanlashni so'raydi: o'zbekcha yoki ruscha.

## Komandalar

- `/start` - ro'yxatdan o'tish va til tanlash
- `/add` - tranzaksiya qo'shish
- `/stats` - joriy oy statistikasi
- `/history` - oxirgi 10 ta tranzaksiya
- `/categories` - kategoriyalarni ko'rish, qo'shish, o'chirish
- `/report` - barcha tranzaksiyalarni CSV formatda olish
- `/limit` - oylik xarajat limitini belgilash
- `/monthly` - oxirgi 3 oy taqqoslash

## Serverda screen bilan ishlatish

```bash
screen -S finbot
source venv/bin/activate
python bot.py
```

Fonda qoldirish: `Ctrl+A`, keyin `D`.

Qayta ulanish:

```bash
screen -r finbot
```
# FINANCE-BOT
