from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import openai

# Установка токена вашего Telegram бота
bot_token = "7054481464:AAFc2fKgQIvx-ywh7zoY_GM41-8R68-pcBQ"

# Убедитесь, что вы правильно вставили свой токен
if not bot_token or bot_token == "YOUR_BOT_TOKEN":
    raise ValueError("Invalid Telegram bot token.")

# Установка токена OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

updater = Updater(bot_token, use_context=True)

# Функция-обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне название фильма, и я предложу о чем поговорить!')

updater.dispatcher.add_handler(CommandHandler("start", start))

# Функция-обработчик сообщений с фильмами
def handle_message(update: Update, context: CallbackContext) -> None:
    film_name = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-003",  # Модель ChatGPT
        prompt=film_name,
        max_tokens=50  # Максимальное количество токенов в ответе
    )
    update.message.reply_text(response.choices[0].text.strip())

updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Основная функция, которая запускает бота
def main() -> None:
    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
