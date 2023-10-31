from aiogram.types import Message, ChatId
import hashlib

HASHED_PASSWORD = "your_hashed_password_here"

@dp.message_handler(commands="auth")
async def auth_command(message: Message):
    await message.answer("Please enter your password:")

@dp.message_handler(lambda message: not message.text.startswith("/"))
async def check_password(message: Message, data: dict):
    entered_password = message.text
    hashed_input = hashlib.sha256(entered_password.encode()).hexdigest()

    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id

    if 'is_authenticated' not in data:
        data['is_authenticated'] = {}

    # Delete the message containing the password
    await dp.bot.delete_message(chat_id=ChatId(chat_id), message_id=message_id)

    if hashed_input == HASHED_PASSWORD:
        data['is_authenticated'][user_id] = True
        await message.answer("You're authenticated!")
    else:
        await message.answer("Incorrect password. Try again.")
