import asyncio
import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command


BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ZaRaZa_Za_RPH.github.io/casino-bot/webapp/index.html")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_balances = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 1000
        await message.answer(
            f"🎰 Привет, {message.from_user.first_name}!\n"
            f"Тебе начислен приветственный бонус: 1000 💎 монет.\n"
            f"Нажми на кнопку ниже, чтобы открыть казино."
        )
    else:
        await message.answer(
            f"С возвращением, {message.from_user.first_name}!\n"
            f"Твой баланс: {user_balances[user_id]} 💎.\n"
            f"Готов испытать удачу?"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🎲 Открыть казино 🎲",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [InlineKeyboardButton(
                text="💰 Проверить баланс",
                callback_data="check_balance"
            )]
        ]
    )
    await message.answer("👇 Нажми на кнопку, чтобы войти в игру:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "check_balance")
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    balance = user_balances.get(user_id, 0)
    await callback_query.message.answer(f"💰 Твой текущий баланс: {balance} 💎")
    await callback_query.answer()

@dp.message(lambda message: message.web_app_data is not None)
async def handle_webapp_data(message: types.Message):
    user_id = message.from_user.id
    data = message.web_app_data.data
    
    try:
        payload = json.loads(data)
        action = payload.get("action")
        
        if action == "init_user":
            balance = user_balances.get(user_id, 0)
            await message.answer(
                f"✅ Вход в казино выполнен!\n"
                f"Твой баланс: {balance} 💎\n"
                f"Играй в мини-приложении и возвращайся за бонусами!"
            )
        
        elif action == "update_balance":
            new_balance = payload.get("balance", 0)
            user_balances[user_id] = new_balance
            logger.info(f"User {user_id} balance updated to {new_balance}")
        
        elif action == "reset_balance":
            new_balance = payload.get("balance", 500)
            user_balances[user_id] = new_balance
            await message.answer(f"🔄 Баланс сброшен! Твой новый баланс: {new_balance} 💎")
            
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from {user_id}")
    except Exception as e:
        logger.error(f"Error handling webapp data: {e}")
        
async def main():
    logger.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
