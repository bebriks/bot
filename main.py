from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен вашего бота
TOKEN = '8056091786:AAHlJYwcbMrfhZXllc-JSM1Egq4Sk3JRnAY'
# ID менеджера, которому будут пересылаться сообщения
MANAGER_CHAT_ID = '7248143106'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    how_it_works_text = """
🔍 Как это работает?

1️⃣ Оставляешь заявку (предмет, тип работы, сроки)
2️⃣ Получаешь расчёт стоимости
3️⃣ Оплачиваешь удобным способом
4️⃣ Получаешь готовую работу в срок

📌 Конфиденциально, безопасно, без предоплат!
"""
    await update.message.reply_text(how_it_works_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Отправляем подтверждение клиенту
        await update.message.reply_text(
            '✅ Ваша заявка принята в работу!\n\n'
            'Наш менеджер свяжется с вами в ближайшее время для уточнения деталей.\n'
            'Если у вас появятся дополнительные вопросы или пожелания - '
            'просто напишите их здесь, мы оперативно их обработаем.'
        )

        # Пересылаем сообщение менеджеру
        await context.bot.forward_message(
            chat_id=MANAGER_CHAT_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")


def main() -> None:
    # Создаём приложение бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler('start', start))
    # Обрабатываем текстовые сообщения и фото
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()