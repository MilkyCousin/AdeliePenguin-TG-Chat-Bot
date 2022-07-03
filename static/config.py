import os

class TelegramClient:
    # key data for bot
    bot_name = "bot-name"
    bot_user_id = "bot-user-id"
    token_id = "bot-token-id"
    # data for feedback chat
    feedback_id = "feedback-chat-id"
    # for webhook
    host = "https://examplehost.com/"
    # path to database
    database_location = os.path.join(
            os.getcwd(), "adeliepenguin_bot", "static", "database", "ChatBotTrace.db"
            )
    # phrases that penguin speaks
    info_txt = "***Надаю важливі абітурієнту посилання:***"
    denied_txt = "Доступ заборонено."
    success_txt = "Дякую за відгук! Подумаю над цим."
    greeting_txt_tuple = (
        "Вітаю у чаті абітурієнтів мех-мату, {firstName}! Для отримання базової інформації, скористайся посиланнями нижче. Якщо є питання, задавай їх експертам у чаті.",
        "Отакої, у нас в чаті {firstName} - давайте привітаємо його! Необхідна інформація за посиланнями нижче.",
        "У чат вривається {firstName}! Бажаємо розібратися йому з усіма питаннями. Базова інформація за посиланнями.",
        "Привіт, {firstName}! Ти в чаті абітурієнтів мех-мату. Необхідна інформація подана нижче. Успіхів!",
        "Це птах? Це літак? Ні, це абітурієнт {firstName} прилетів до нашого чату! Основна інформаця подана нижче."
        )
    greeting_length = len(greeting_txt_tuple)
    start_txt = "Привіт! Я пінгвін Аделі. Якщо ти мех-матівська абітура, то для отримання важливої інформації скористайся командами."
    dontknow_txt_tuple = (
        "Я вас не розумію.",
        "Шо? А простіше можна?",
        "Відповідь не така. Подумайте трохи.",
        "Мех-мат це круто!"
        )
    dontknow_length = len(dontknow_txt_tuple)
    text = ["📕 Все про вступ 2022",
            "🧮 Гайд про математику",
            "📊 Гайд про статистику",
            "💻 Гайд про компмат",
            "🐧 Мєми про математику"]
    link = ["link-1",
            "link-2",
            "link-3",
            "link-4",
            "link-5"]
    # max connections for bot
    max_connections = 20

