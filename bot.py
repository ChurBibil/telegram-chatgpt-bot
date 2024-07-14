from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
import os

app = Flask(__name__)

# Установка токена вашего Telegram бота
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Убедитесь, что переменная окружения установлена правильно
if not bot_token:
    raise ValueError("Invalid Telegram bot token.")

bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot, None, use_context=True)

# Словарь для хранения списка фильмов и сериалов
films = {
    'to_watch': [],
    'watched': []
}

# Функция-обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я помогу тебе записывать фильмы и сериалы для просмотра. '
                              'Используй /add для добавления в список, /watched для отметки просмотренных, '
                              'и /list для просмотра списков.')

dispatcher.add_handler(CommandHandler("start", start))

# Функция-обработчик команды /add для добавления фильма или сериала в список для просмотра
def add(update: Update, context: CallbackContext) -> None:
    msg = update.message.text.split(' ', 1)
    if len(msg) == 2:
        film_name = msg[1]
        if film_name not in films['to_watch'] and film_name not in films['watched']:
            films['to_watch'].append(film_name)
            update.message.reply_text(f'Фильм/сериал "{film_name}" добавлен в список для просмотра.')
        else:
            update.message.reply_text(f'Фильм/сериал "{film_name}" уже добавлен в список.')
    else:
        update.message.reply_text('Используйте команду /add <название фильма или сериала>.')

dispatcher.add_handler(CommandHandler("add", add))

# Функция-обработчик команды /watched для отметки просмотренного фильма или сериала
def watched(update: Update, context: CallbackContext) -> None:
    msg = update.message.text.split(' ', 1)
    if len(msg) == 2:
        film_name = msg[1]
        if film_name in films['to_watch']:
            films['to_watch'].remove(film_name)
            films['watched'].append(film_name)
            update.message.reply_text(f'Фильм/сериал "{film_name}" отмечен как просмотренный.')
        elif film_name in films['watched']:
            update.message.reply_text(f'Фильм/сериал "{film_name}" уже отмечен как просмотренный.')
        else:
            update.message.reply_text(f'Фильм/сериал "{film_name}" не найден в списке.')
    else:
        update.message.reply_text('Используйте команду /watched <название фильма или сериала>.')

dispatcher.add_handler(CommandHandler("watched", watched))

# Функция-обработчик команды /list для вывода списков фильмов и сериалов
def list_films(update: Update, context: CallbackContext) -> None:
    to_watch_str = "\n".join(films['to_watch']) if films['to_watch'] else "Список для просмотра пуст."
    watched_str = "\n".join(films['watched']) if films['watched'] else "Список просмотренных пуст."
    update.message.reply_text(f'<b>Список для просмотра:</b>\n{to_watch_str}\n\n<b>Список просмотренных:</b>\n{watched_str}',
                              parse_mode='HTML')

dispatcher.add_handler(CommandHandler("list", list_films))

@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def set_webhook():
    webhook_url = 'https://telegram-chatgpt-bot-3ai3.onrender.com/hook'  # Замените на URL вашего сервера
    bot.set_webhook(webhook_url)

if __name__ == '__main__':
    set_webhook()
    app.run(port=8443)
