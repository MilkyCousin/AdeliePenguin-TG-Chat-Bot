from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import static.config as cfg


class TelegramAPIClient:

    def __init__(self, bot_entity: Bot, text=None, link=None):
        self.__bot = bot_entity
        self._buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=text[j], url=link[j])] for j in range(len(link))]
        )

    def send_message(self, chat_id, text="", with_keys=False, parse_mode="Markdown"):
        msg = self.__bot.sendMessage(
            chat_id=chat_id, text=text, parse_mode=parse_mode,
            reply_markup=self._buttons if with_keys else None
        )
        return msg

    def delete_message(self, chat_id, message_id):
        self.__bot.deleteMessage(
            chat_id = chat_id, message_id = message_id
            )

    def set_webhook(self, host):
        self.__bot.set_webhook(
            url=host, max_connections=cfg.TelegramClient.max_connections
            )
