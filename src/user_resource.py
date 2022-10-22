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
        conn.close()

        return user

    @staticmethod
    def get_all():
        sql = f"SELECT * FROM {database}.{table}"
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        users = cur.fetchall()
        conn.close()

        return users

    @staticmethod
    def get_users_by_params(params):
        sql = f'SELECT * FROM {database}.{table} WHERE '
        email = params.get('email', '')
        first_name = params.get('first_name', '')
        last_name = params.get('last_name', '')

        if email:
            sql += f'email="{email}" and '
        if first_name:
            sql += f'first_name="{first_name}" and '
        if last_name:
            sql += f'last_name="{last_name}" and '

        sql = sql[:-5]
        sql += ';'
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        users = cur.fetchall()
        conn.close()

        return users

    @staticmethod
    def sign_up_user(email, password, first_name, last_name):
        sql = f"INSERT INTO {database}.{table}(email, password, first_name, last_name) " \
              f"VALUES (\"{email}\", \"{password}\", \"{first_name}\", \"{last_name}\")"
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.close()

    @staticmethod
    def delete_user(uid):
        sql = f"DELETE FROM {database}.{table} WHERE uid={uid}"
        conn = UserResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.close()

    @staticmethod
    def update_user(uid, request_json):
        if len(request_json) > 0:
            email = request_json.get('email', '')
            password = request_json.get('password', '')
            first_name = request_json.get('first_name', '')
            last_name = request_json.get('last_name', '')

            sql = f"UPDATE {database}.{table} SET "
            if email:
                sql += f'email="{email}", '
            if password:
                sql += f'password="{password}", '
            if first_name:
                sql += f'first_name="{first_name}", '
            if last_name:
                sql += f'last_name="{last_name}", '
            sql = sql[:-2]
            sql += f' WHERE uid={uid};'

            conn = UserResource._get_connection()
            cur = conn.cursor()
            cur.execute(sql)
            conn.close()
