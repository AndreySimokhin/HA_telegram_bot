from pathlib import Path
from telebot import TeleBot
from telebot.types import InputFile


class Telegram_Bot:
    @staticmethod
    def initialize(token: str):
        Telegram_Bot.bot = TeleBot(token)

    @staticmethod
    def send_file(filepath: str, chat_id: int):
        file = Path(filepath)
        if file.suffix in ('mp4', '.mp4'):
            return Telegram_Bot.bot.send_video(chat_id, video=InputFile(file))
        Telegram_Bot.bot.send_document(chat_id, document=InputFile(file))
