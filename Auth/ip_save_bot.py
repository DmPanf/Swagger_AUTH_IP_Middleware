from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor

bot = Bot(token="YOUR_BOT_TOKEN_HERE")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ALLOWED_USER_ID = 123456789  # Замените на ваш Telegram User ID

async def send_message_to_admin(*args, **kwargs):
    await bot.send_message(chat_id=ALLOWED_USER_ID, text="Bot started")

@dp.message_handler(lambda message: message.from_user.id == ALLOWED_USER_ID, commands=["add_ip"])
async def add_ip(message: types.Message):
    ip_address = message.get_args()
    if not ip_address:
        await message.reply("Please provide an IP address.")
        return

    # Добавляем IP-адрес в .env или другой конфигурационный файл
    with open(".env", "a") as f:
        f.write(f"\nALLOWED_IP={ip_address}")

    await message.reply(f"IP address {ip_address} added.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, on_startup=send_message_to_admin)
