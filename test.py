import sqlite3


#conn = sqlite3.connect('flats.db')
#cur = conn.cursor()
#cur.execute("UPDATE flats set status = 1 where status = 0;")

conn = sqlite3.connect('flats.db')
cur = conn.cursor()
cur.execute("SELECT * FROM flats;")
one_result = cur.fetchall()
for i in one_result:
    print(i)


#cur.execute(f"SELECT flat_id FROM flats WHERE flat_id = {id[0]};")
#cur.fetchall()

conn.commit()




def delete_multiple_records(ids_list):
    try:
        sqlite_connection = sqlite3.connect('flats.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_update_query = """DELETE from flats where status = 0"""
        cursor.execute(sqlite_update_query)
        sqlite_connection.commit()
        print("Удалено записей:", cursor.rowcount)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

ids_to_delete = 0
delete_multiple_records(ids_to_delete)


