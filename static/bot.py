from static.telegram_client import TelegramAPIClient
from static.database import DatabaseClass
from telegram import Bot
from telegram.error import BadRequest
from random import randint
import static.config as cfg
import re


class AppManager:

    def __init__(
        self, bot_api=cfg.TelegramClient.token_id, host=cfg.TelegramClient.host
        ):
        self._bot = Bot(token=bot_api)

        self._path_to_db = cfg.TelegramClient.database_location
        self._db = DatabaseClass(self._path_to_db)

        self._telegram_client = TelegramAPIClient(
            bot_entity=self._bot,
            text=cfg.TelegramClient.text,
            link=cfg.TelegramClient.link
        )
        self._telegram_client.set_webhook(host)

        self._commands = {
            "/start":
                {"cmd": self.handle_start, "params": 0},
            "/get_links":
                {"cmd": self.handle_get_links, "params": 0},
            "/broadcast":
                {"cmd": self._handle_broadcast, "params": 1},
            "/feedback":
                {"cmd": self._handle_feedback, "params": 1},

            "/start@" + cfg.TelegramClient.bot_name:
                {"cmd": self.handle_start, "params": 0},
            "/get_links@" + cfg.TelegramClient.bot_name:
                {"cmd": self.handle_get_links, "params": 0}
        }

        self._update = None
        self._txt = None

        self._cur_chat_id = None
        self._cur_chat_type = None
        self._cur_sender_id = None

        self._new_user_id = None
        self._new_first_name = None

    def handle_greeting(self):
        # try to overcome markdown injection thing
        cur_first_name = re.sub("\]", "", self._new_first_name)
        cur_first_name = re.sub("\[", "", cur_first_name)
        # put relooked first name in text
        textFormat = "[" + cur_first_name + "](tg://user?id=" + self._new_user_id + ")"
        msg_to_send_blank = cfg.TelegramClient.greeting_txt_tuple[
                randint(0, cfg.TelegramClient.greeting_length-1)
                ]
        msg_to_send = msg_to_send_blank.format(firstName=textFormat)
        # send it
        self._write_message(msg=msg_to_send, wkeys=True)

    def handle_get_links(self):
        self._write_message(msg=cfg.TelegramClient.info_txt, wkeys=True)

    def handle_start(self):
        if self._cur_chat_type == "private":
            self._telegram_client.send_message(
            chat_id=self._cur_chat_id,
            text=cfg.TelegramClient.start_txt,
            with_keys=False
            )

    def _handle_addition(self):
        self._db.append_data_chat(self._cur_chat_id, self._cur_chat_type)

    def handle_trash(self):
        self._telegram_client.send_message(
            chat_id = self._cur_chat_id,
            text=cfg.TelegramClient.dontknow_txt_tuple[
                randint(0, cfg.TelegramClient.dontknow_length-1)
                ],
            with_keys=False
            )

    def _handle_broadcast(self):
        if self._cur_chat_type == "private":
            if self._db.check_is_admin(self._cur_sender_id):
                chats = self._db.retreive_chats
                for chat in chats:
                    if chat[1] != "private":
                        try:
                            cur_msg = self._telegram_client.send_message(
                                chat_id=chat[0],
                                text=self._txt[1],
                                with_keys=False
                                )
                            cur_msg_id = cur_msg.message_id
                            # add to messages
                            self._db.append_data_msg(
                                chat[0], cur_msg_id,
                                cfg.TelegramClient.bot_user_id, 1
                                )
                        except BadRequest:
                            print("todo")
            else:
                self._telegram_client.send_message(
                    chat_id=self._cur_chat_id,
                    text=cfg.TelegramClient.denied_txt,
                    with_keys=False
                    )

    def _handle_feedback(self):
        txt_to_send = self._txt[1]

        if self._cur_chat_type == "private":
            # to feedback chat
            self._telegram_client.send_message(
                chat_id=cfg.TelegramClient.feedback_id,
                text="***Feedback***:\n" + txt_to_send,
                with_keys=False
                )
            # to private chat
            self._telegram_client.send_message(
                chat_id=self._cur_chat_id,
                text=cfg.TelegramClient.success_txt,
                with_keys=False
                )

    def _delete_old_msg(self, chat_id, chat_type, sender_id):
        if chat_type != "private":
            q_result = self._db.get_msg_by_user_and_chat(chat_id, sender_id)
            if bool(q_result):
                for j in range(len(q_result)):
                    try:
                        self._telegram_client.delete_message(chat_id, q_result[j][1])
                    except BadRequest as e:
                        print("{}: Encountered non-available message".format(e))
            self._db.delete_msg_by_user(sender_id, chat_id)

    def _write_message(self, msg, wkeys=False):
        # remove older messages
        self._delete_old_msg(
            chat_id=self._cur_chat_id,
            chat_type=self._cur_chat_type,
            sender_id=cfg.TelegramClient.bot_user_id
            )
        # send new message
        cur_msg = self._telegram_client.send_message(
            chat_id=self._cur_chat_id, text=msg, with_keys=wkeys
            )
        cur_msg_id = cur_msg.message_id
        # add to messages
        self._db.append_data_msg(
            self._cur_chat_id, cur_msg_id, cfg.TelegramClient.bot_user_id, 1
            )

    def handle_message(self, update):
        # get current update in chat
        self._update = update

        if "message" not in self._update:
            return None

        self._cur_chat_id = self._update["message"]["chat"]["id"]
        self._cur_chat_type = self._update["message"]["chat"]["type"]
        self._cur_sender_id = self._update["message"]["from"]["id"]

        if "new_chat_member" in self._update["message"]:
            self._new_first_name = self._update["message"]["new_chat_member"]["first_name"]
            self._new_user_id = str(self._update["message"]["new_chat_member"]["id"])

            if self._new_user_id == cfg.TelegramClient.bot_user_id:
                return self._handle_addition()

            return self.handle_greeting()

        if 'text' not in self._update["message"]:
            return None

        self._txt = re.split(" ", self._update["message"]["text"], 1)
        par_len = (len(self._txt) - 1)

        for command in self._commands:
            par_exp = self._commands[command]["params"]
            if bool(re.fullmatch(command, self._txt[0])) and (par_len == par_exp):
                apply_cmd = self._commands[command]["cmd"]
                return apply_cmd()

        if self._update["message"]["chat"]["type"] == "private":
            self.handle_trash()
