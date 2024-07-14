import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токен и chat_id из переменных окружения
TOKEN = os.getenv("TOKEN")
YOUR_CHAT_ID = int(os.getenv("YOUR_CHAT_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Мой дорогой чурбибиль, напиши че ты там хочешь глянуть ну или спроси какую-нибудь залупу, я к твоим услугам даже если сплю или занят')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    # Проверка на наличие ссылки на фильм
    if 'http' in text:
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=f'Фильм: {text}')
        await update.message.reply_text('Понял, глянем')
    else:
        # Отправляем запрос в ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=150
        )
        reply = response.choices[0].text.strip()
        await update.message.reply_text(reply)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
