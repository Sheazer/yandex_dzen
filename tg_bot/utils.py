from telegram import Bot
from telegram.error import TelegramError



def send_telegram_message(chat_id):
    message = "Ваш пост опубликован"
    token = "7737861074:AAG1h_x5FrmzzhZR7WPX5Wn1jqr1Fq9LvP8"

    bot = Bot(token=token)

    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")


