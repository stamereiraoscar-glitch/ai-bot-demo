import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "898036971"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-nano")

COMPANY_NAME = os.getenv("COMPANY_NAME", "Demo AI Bot")
LANGUAGE = os.getenv("LANGUAGE", "RU")

TEXTS = {
    "RU": {
        "start": f"Здравствуйте! Добро пожаловать в {COMPANY_NAME} 👋\n\nНапишите сообщение, и AI ответит вам.\n\nКнопки ниже помогут очистить диалог или открыть помощь.",
        "help": "Этот бот отвечает на ваши сообщения с помощью AI.\n\nКнопки:\n🧹 Очистить диалог — удаляет историю текущего диалога\nℹ️ Помощь — показывает это сообщение",
        "cleared": "История диалога очищена ✅",
        "thinking": "Думаю…",
        "error": "Произошла ошибка при обращении к AI. Попробуйте ещё раз.",
        "empty": "Напишите любой вопрос или сообщение.",
        "clear_button": "🧹 Очистить диалог",
        "help_button": "ℹ️ Помощь"
    },
    "EN": {
        "start": f"Welcome to {COMPANY_NAME} 👋\n\nSend a message and the AI will reply.\n\nUse the buttons below to clear the chat or open help.",
        "help": "This bot replies to your messages using AI.\n\nButtons:\n🧹 Clear dialogue — clears the current chat history\nℹ️ Help — shows this message",
        "cleared": "Dialogue history cleared ✅",
        "thinking": "Thinking…",
        "error": "There was an error while contacting the AI. Please try again.",
        "empty": "Send any question or message.",
        "clear_button": "🧹 Clear dialogue",
        "help_button": "ℹ️ Help"
    }
}
