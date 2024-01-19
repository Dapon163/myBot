import psycopg2
from psycopg2 import sql
from Pg_conf import host, port, user, password, db_name
from datetime import date, timedelta


class Pg_class:
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        cursor = connection.cursor()

        def commit(self):
            self.connection.commit()

        # <-------------------------------------------------------Блок регистрации------------------------------------->
        def reg(self, data: tuple):
            request = "INSERT INTO clients (id, username, name) VALUES (%s, %s, %s)"
            self.cursor.execute(request, data)
            self.connection.commit()

        def check_id(self, client_id: str):
            request = "SELECT id FROM clients WHERE id = %s"
            self.cursor.execute(request, (client_id,))
            return self.cursor.fetchone()

        def rename(self, client_id, username, name):
            request = "UPDATE clients SET username = %s, name = %s where id = %s"
            self.cursor.execute(request, (username, name, client_id))
            self.connection.commit()

        # <------------------------------------------------------------------------------------------------------------>
        def get_name(self, id):
            request = "SELECT name FROM clients WHERE id = %s"
            self.cursor.execute(request, (id,))
            return self.cursor.fetchone()[0]

        # <--------------------------------------------------Запись репы в бд------------------------------------------>
        def apply_repetition(self, table: str, data: tuple):
            request = "UPDATE {table} SET book = %s, client_id = %s, type = %s WHERE date = %s AND hour = %s"
            self.cursor.execute(sql.SQL(request).format(table=sql.Identifier(table)), data)
            self.connection.commit()

        # <--------------------------------------------------Доступные часы-------------------------------------------->
        def select_hours(self, table: str, day: tuple):
            request = "SELECT hour FROM {table} WHERE book = false AND date = %s;"
            self.cursor.execute(sql.SQL(request).format(table=sql.Identifier(table)), day)
            ugly_tuple = self.cursor.fetchall()
            return tuple(x[0] for x in ugly_tuple)

        # <----------------------------------------------Скрипт на заполнение дней------------------------------------->
        def set_new_days(self):
            list_days = {0: 'monday', 1: 'tuesday', 2: 'wednesday',
                         3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}
            for i in range(7):
                table = list_days[i]
                for j in range(10, 22, 1):
                    request = "INSERT INTO {table} (date, hour, book, client_id, type)" \
                              " VALUES (%s, %s, false, NULL, NULL);"
                    self.cursor.execute(sql.SQL(request).format(table=sql.Identifier(table)),
                                        (date.today() - timedelta(days=date.today().weekday() - i), j))
            self.connection.commit()

        # <--------------------------------------Поиск и отмена забронированных репетиций------------------------------>
        def search_repetition(self, client_id: str, table: str):
            request = f"SELECT hour FROM {table} WHERE client_id = {client_id}"
            self.cursor.execute(request)
            ugly_tuple = self.cursor.fetchall()
            return tuple(x[0] for x in ugly_tuple)
    except Exception as _ex:
        print('[ERR] Error while working with PostgreSQL:\n', _ex)
