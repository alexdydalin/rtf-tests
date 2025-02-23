from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from models import db, Message
from bot import TelegramBot
from dotenv import load_dotenv
import os
import threading
import asyncio

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)

# Инициализация SocketIO
socketio = SocketIO(app, async_mode='threading')

# Создание экземпляра бота
telegram_bot = TelegramBot(app, socketio)

# Создание отдельного event loop для бота
bot_loop = asyncio.new_event_loop()


@app.route('/')
def index():
    with app.app_context():
        messages = Message.query.order_by(Message.id.asc()).all() # получение всех сообщений из бд
    return render_template('index.html', messages=messages) # отображение шаблона и истории


@app.route('/send', methods=['POST'])
def send_message():
    user_id = request.form.get('user_id')
    text = request.form.get('text')

    user_id = int(user_id)

    with app.app_context():
        # сохранение сообщения от бота
        msg = Message(
            user_id=user_id,
            text=text.strip(),
            is_bot=True
        )
        db.session.add(msg)
        db.session.commit()

        # отправка сообщения из веба в бота
        asyncio.run_coroutine_threadsafe(
            telegram_bot.bot.send_message(user_id, text),
            bot_loop
        )

        # отправка сообщения из тг в веб интерфейс
        socketio.emit('new_message', {
            'user_id': user_id,
            'text': text,
            'is_bot': True
        })

    return redirect(url_for('index'))



# запуск бота
def run_bot():
    asyncio.set_event_loop(bot_loop)
    bot_loop.run_until_complete(telegram_bot.start_polling())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запуск Flask-приложения
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)