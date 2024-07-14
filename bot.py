from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Установка токена вашего Telegram бота
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

CHAT_ID = os.getenv('694294456')

# Функция для отправки уведомления
def send_notification(message):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)


# Убедитесь, что переменная окружения установлена правильно
if not bot_token:
    raise ValueError("Invalid Telegram bot token.")

# Словарь для хранения списка фильмов и сериалов
films = {
    'to_watch': [],
    'watched': []
}

# Функция-обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет котёнок, крч пока ты в рилсах бальзамируешься, то находишь фильмы и сериалы, вот сюда их и ебашь, посмотрим" '
                              'Используй /add для добавления в список, /watched для отметки просмотренных, '
                              'и /list для просмотра списков.')

# Функция-обработчик команды /add для добавления фильма или сериала в список для просмотра
def add(update: Update, context: CallbackContext) -> None:
    msg = update.message.text.split(' ', 1)
    if len(msg) == 2:
        film_name = msg[1]
        if film_name not in films['to_watch'] and film_name not in films['watched']:
            films['to_watch'].append(film_name)
            update.message.reply_text(f'Фильм/сериал "{film_name}" уже в моей голове.')
        else:
            update.message.reply_text(f'Фильм/сериал "{film_name}" уже добавлен в список.')
    else:
        update.message.reply_text('Используй команду /add <название фильма или сериала>.')

# Функция-обработчик команды /watched для отметки просмотренного фильма или сериала
def watched(update: Update, context: CallbackContext) -> None:
    msg = update.message.text.split(' ', 1)
    if len(msg) == 2:
        film_name = msg[1]
        if film_name in films['to_watch']:
            films['to_watch'].remove(film_name)
            films['watched'].append(film_name)
            update.message.reply_text(f'Фильм/сериал "{film_name}" уже смотрели, че ебнулась.')
        elif film_name in films['watched']:
            update.message.reply_text(f'Фильм/сериал "{film_name}" смотрели мы, альцгеймерша.')
        else:
            update.message.reply_text(f'Фильм/сериал "{film_name}" не найден в списке.')
    else:
        update.message.reply_text('Используйте команду /watched <название фильма или сериала>.')

# Функция-обработчик команды /list для вывода списков фильмов и сериалов
def list_films(update: Update, context: CallbackContext) -> None:
    to_watch_str = "\n".join(films['to_watch']) if films['to_watch'] else "Нихуя нет еще."
    watched_str = "\n".join(films['watched']) if films['watched'] else "Еще нихуя нет."
    update.message.reply_text(f'<b>Список для просмотра:</b>\n{to_watch_str}\n\n<b>Список просмотренных:</b>\n{watched_str}',
                              parse_mode='HTML')

# Функция для обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Кись, ну че думаешь я илон маск, хуйню не неси, заново давай. Используй /start для начала работы.')

def main() -> None:
    # Создаем Updater и передаем ему токен вашего бота
    updater = Updater(bot_token)

    # Получаем диспетчер от Updater
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("watched", watched))
    dispatcher.add_handler(CommandHandler("list", list_films))

    # Регистрируем обработчик сообщений, который реагирует на текстовые сообщения
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запускаем polling
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
