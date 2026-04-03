import mysql.connector
from mysql.connector import Error


class DbConnector:
    def __init__(self, settings):
        self.database_type = settings["database_type"]
        self.host = settings["host"]
        self.port = settings["port"]
        self.user_name = settings["user_name"]
        self.password = settings["password"]
        self.database = settings["database"]
        self.is_connect = False
        self.message = "未接続"

    def connect(self):
        if self.database_type == "MySQL":
            self.connect_mysql()
        return self.is_connect, self.message

    def connect_mysql(self):
        try:
            self.connection = mysql.connector.connect(
                # host=self.host,
                # port=self.port,
                # user=self.user_name,
                # password=self.password,
                # database=self.database,
                host="127.0.0.1",
                port="3306",
                user="root",
                password="password",
                database="term2",
            )
            print("test")
            if self.connection.is_connected():
                self.is_connect = True
                self.message = "正常に接続されました"

        except Error as e:
            self.connection = False
            self.message = f"接続エラー: {e}"
