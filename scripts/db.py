import sqlite3


def get_connection():
    name = '../scrapers/drugscom/drugs.sqlite3'
    connection = None
    connection = sqlite3.connect(name)
    return connection


def select_nodes():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT brand,ingredient,drug_class FROM products'
    cursor.execute(sql)
    records = cursor.fetchall()
    return records
