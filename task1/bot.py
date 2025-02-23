from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from models import db, Message

load_dotenv()


class TelegramBot:
    def __init__(self, app, socketio):
        self.bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN')) # создание экземпляра бота
        self.dp = Dispatcher() # создание диспетчера для обработки сообщений
        self.app = app
        self.socketio = socketio

        # регистрация обработчиков команды start и сообщений
        self.dp.message.register(self.handle_start, Command(commands=['start']))
        self.dp.message.register(self.handle_message) # обработка всех сообщений

        # регистрация обработчиков жизненного цикла
        self.dp.startup.register(self.on_startup)
        self.dp.shutdown.register(self.on_shutdown)

    async def on_startup(self):
        print("бот активен")

    async def on_shutdown(self):
        print("бот остановлен")
        await self.bot.session.close() # закрытие сессии работы с ботом

    async def handle_start(self, message: types.Message):
        await message.answer("напиши собщение") # ответ на start
        with self.app.app_context():
            self._send_to_web(message.from_user.id, "бот активирован", is_bot=True)

    async def handle_message(self, message: types.Message):
        with self.app.app_context():
            # сохранение сообщения в бд
            msg = Message(
                user_id=message.from_user.id,
                text=message.text,
                is_bot=False
            )
            db.session.add(msg)
            db.session.commit()

            # отправка сообщения в веб интерфейс
            self._send_to_web(message.from_user.id, message.text, is_bot=False)

    def _send_to_web(self, user_id: int, text: str, is_bot: bool):
        # отправка события через socketio
        self.socketio.emit('new_message', {
            'user_id': user_id,
            'text': text,
            'is_bot': is_bot
        })

    async def start_polling(self):
        # запуск полинга тг сервера
        await self.dp.start_polling(
            self.bot,
            allowed_updates=self.dp.resolve_used_update_types(),
            close_bot_session=True
        )