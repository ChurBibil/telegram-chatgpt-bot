import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

app = Flask(__name__)

# Установка токена вашего Telegram бота
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Убедитесь, что переменные окружения установлены правильно
if not bot_token:
    raise ValueError("Invalid Telegram bot token.")
if not openai.api_key:
    raise ValueError("Invalid OpenAI API key.")

bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot, None, use_context=True)

# Функция-обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне название фильма, и я предложу о чем поговорить!')

dispatcher.add_handler(CommandHandler("start", start))

# Функция-обработчик сообщений с фильмами
def handle_message(update: Update, context: CallbackContext) -> None:
    film_name = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-003",  # Модель ChatGPT
        prompt=film_name,
        max_tokens=50  # Максимальное количество токенов в ответе
    )
    update.message.reply_text(response.choices[0].text.strip())

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def set_webhook():
    webhook_url = 'https://my-awesome-bot.onrender.com/hook'  # Замените на URL вашего сервера
    bot.set_webhook(webhook_url)

if __name__ == '__main__':
    set_webhook()
    app.run(port=8443)
