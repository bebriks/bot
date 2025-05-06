from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

API_URL = "http://localhost:8000/ask"


async def start(update: Update, context):
    await update.message.reply_text("Привет! Задайте вопрос по FAQ:")


async def handle_message(update: Update, context):
    try:
        response = requests.post(
            API_URL,
            json={"question": update.message.text}
        ).json()

        await update.message.reply_text(response.get("answer", "Не удалось получить ответ"))
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main():

    application = Application.builder().token("7678692952:AAHuSebVd3VxJVO8ex3K7bDhCFrttbjk4VM").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
