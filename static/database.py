import os
import sqlite3
import datetime

class DatabaseClass:

    def __init__(self, db_path):

        self.__path = db_path

    def __set_connection_and_cursor(self):

        conn = sqlite3.connect(self.__path)
        return conn, conn.cursor()

    def __close(self, conn, append_mode=False):

        if append_mode:
            conn.commit()
        conn.close()

    def _exists_keys(self, chat_id, chat_type):

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """SELECT * FROM Chats WHERE (Id=?) AND (Type=?)""",
            (chat_id, chat_type, )
            )
        res = bool(curs.fetchall())
        self.__close(conn)
        return res

    def append_data_chat(self, chat_id, chat_type):

        if self._exists_keys(chat_id, chat_type):
            return None

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """INSERT INTO Chats VALUES (?, ?)""",
            (chat_id, chat_type, )
            )
        self.__close(conn, append_mode=True)

    def append_data_msg(self, chat_id, message_id, sender_id, sender_is_bot):

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """INSERT INTO Messages VALUES (?, ?, ?, ?, ?)""",
            (chat_id, message_id, sender_id, sender_is_bot, str(datetime.datetime.now()), )
            )
        self.__close(conn, append_mode=True)

    def delete_msg_by_user(self, user_id, chat_id):

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """DELETE FROM Messages WHERE (Chat_Id=?) AND (Sender_Id=?)""",
            (chat_id, user_id, )
            )
        self.__close(conn, append_mode=True)

    def delete_msg_by_id(self, chat_id):

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """DELETE FROM Messages WHERE (Chat_Id=?)""", (chat_id, )
            )
        self.__close(conn, append_mode=True)

    def delete_chat_by_id(self, chat_id):

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """DELETE FROM Chats WHERE (Id=?)""", (chat_id, )
            )
        self.__close(conn, append_mode=True)

    def get_msg_by_user_and_chat(self, chat_id, user_id):

        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """SELECT Chat_Id, Message_Id FROM Messages WHERE (Chat_Id=?) AND (Sender_Id=?)""",
            (chat_id, user_id, )
            )
        res = curs.fetchall()
        self.__close(conn)

        return res

    def check_is_admin(self, user_id):
        conn, curs = self.__set_connection_and_cursor()
        curs.execute(
            """SELECT Sum(Case when (User_Id=?) then 1 else 0 end) FROM Admins""",
            (user_id, )
            )
        res = curs.fetchall()[0][0]
        self.__close(conn)
        return res

    @property
    def retreive_chats(self):
        conn, curs = self.__set_connection_and_cursor()
        curs.execute("""SELECT * FROM Chats""")
        res = curs.fetchall()
        self.__close(conn)
        return res
