import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

BOT_TOKEN = "8545757387:AAG_ZLJ-VrhzDbEEHRwIr7ZOO3bia_nwnVE"
WEBAPP_URL = "https://ZaRaZa_Za_RPH.github.io/casino-bot/webapp/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_balances = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id not in user_balances:
        user_balances[message.from_user.id] = 1000
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Открыть казино", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(f"Привет! Твой баланс: {user_balances[message.from_user.id]} 💎", reply_markup=keyboard)

@dp.message(lambda m: m.web_app_data)
async def handle_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    if data.get("action") == "update_balance":
        user_balances[message.from_user.id] = data.get("balance", 0)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())