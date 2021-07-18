import os
import sqlite3

PATH = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(PATH, 'db.sqlite')


def init_db():
    connection = sqlite3.connect(DB)
    connection.execute("""
    CREATE TABLE IF NOT EXISTS place(
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT,
        details TEXT,
        longitude REAL,
        latitude REAL
    )
    """)
    connection.commit()
    connection.close()


def connect():
    init_db()
    return sqlite3.connect(DB)


def add_place(place):
    connection = connect()
    sql = "INSERT INTO place(name, details, longitude, latitude) values(?,?,?,?)"
    cursor = connection.cursor()
    cursor.execute(sql, [place.name, place.details or '', place.longitude, place.latitude])
    new_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return new_id


def get_place_list():
    connection = connect()
    sql = "SELECT * FROM place"
    cursor = connection.cursor()
    cursor.execute(sql)
    place_records = cursor.fetchall()
    places = list(map(lambda x: format_place(cursor, x), place_records))
    connection.close()
    return places


def get_place(place_id):
    connection = connect()
    cursor = connection.cursor()
    sql = "SELECT * FROM place WHERE id  = ?"
    cursor = cursor.execute(sql, [place_id])
    place_record = cursor.fetchone()
    place = format_place(cursor, place_record)
    connection.close()
    return place


def format_place(cursor, place_record):
    names = [description[0] for description in cursor.description]
    place = {}
    for column in zip(names, place_record):
        place[column[0]] = column[1]
    return place
