import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from openai import OpenAI
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=config.OPENAI_API_KEY)

lang = config.LANGUAGE

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=config.TEXTS[lang]["clear_button"])],
        [KeyboardButton(text=config.TEXTS[lang]["help_button"])]
    ],
    resize_keyboard=True
)

# Простая память диалогов в RAM
# Ключ = user_id, значение = список сообщений
user_dialogues = {}

SYSTEM_PROMPT = (
    "You are a helpful AI assistant inside a Telegram bot. "
    "Answer clearly, briefly, and politely. "
    "If the user writes in Russian, answer in Russian. "
    "If the user writes in English, answer in English."
)

@dp.message(Command("start"))
async def start(message: Message):
    user_dialogues[message.from_user.id] = []
    await message.answer(
        config.TEXTS[lang]["start"],
        reply_markup=menu
    )

@dp.message(F.text == config.TEXTS[lang]["help_button"])
async def help_command(message: Message):
    await message.answer(
        config.TEXTS[lang]["help"],
        reply_markup=menu
    )

@dp.message(F.text == config.TEXTS[lang]["clear_button"])
async def clear_dialogue(message: Message):
    user_dialogues[message.from_user.id] = []
    await message.answer(
        config.TEXTS[lang]["cleared"],
        reply_markup=menu
    )

@dp.message()
async def ai_reply(message: Message):
    text = (message.text or "").strip()

    if not text:
        await message.answer(
            config.TEXTS[lang]["empty"],
            reply_markup=menu
        )
        return

    user_id = message.from_user.id

    if user_id not in user_dialogues:
        user_dialogues[user_id] = []

    if len(user_dialogues[user_id]) > 12:
        user_dialogues[user_id] = user_dialogues[user_id][-12:]

    user_dialogues[user_id].append({
        "role": "user",
        "content": text
    })

    try:
        wait_msg = await message.answer(
            config.TEXTS[lang]["thinking"],
            reply_markup=menu
        )

        input_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + user_dialogues[user_id]

        response = client.responses.create(
            model=config.MODEL_NAME,
            input=input_messages
        )

        answer = response.output_text.strip()

        if not answer:
            answer = config.TEXTS[lang]["error"]

        user_dialogues[user_id].append({
            "role": "assistant",
            "content": answer
        })

        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
        await message.answer(answer, reply_markup=menu)

    except Exception as e:
        await bot.send_message(
            config.ADMIN_ID,
            f"⚠️ AI bot error\n\nUser: {message.from_user.full_name}\n"
            f"User ID: {message.from_user.id}\n\nError:\n{e}"
        )
        await message.answer(
            config.TEXTS[lang]["error"],
            reply_markup=menu
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
