import os
import pymysql

database = 'users'
table = 'users'


class UserResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        user = os.environ.get("DBUSER")
        password = os.environ.get("DBPW")
        host = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=user,
            password=password,
            host=host,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):
        sql = f"SELECT * FROM {database}.{table} where uid={key}"
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        user = cur.fetchone()

        return user

    @staticmethod
    def get_all():
        sql = f"SELECT * FROM {database}.{table}"
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        users = cur.fetchall()

        return users
