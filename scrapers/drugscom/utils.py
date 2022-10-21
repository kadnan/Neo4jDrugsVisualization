import sqlite3


def get_connection():
    name = 'drugs.sqlite3'
    connection = None
    connection = sqlite3.connect(name)
    return connection


def store_ingredient_links(link, text, original_url, connection):
    sql = 'INSERT OR IGNORE INTO ingredients (url,name,original_url) VALUES(?,?,?)'
    cursor = connection.cursor()
    cursor.execute(sql, (link, text, original_url,))
    connection.commit()


def store_brand_products(records, connection):
    cursor = connection.cursor()
    for record in records:
        sql = 'INSERT OR IGNORE INTO products (ingredient_url,brand,drug_class,ingredient) VALUES(?,?,?,?)'
        cursor.execute(sql, (record['ingredient_url'], record['brand'], record['drug_name'], record['ingredient'],))
        connection.commit()

        sql = "UPDATE {} set status = 3 where url = '{}' ".format('ingredients', record['ingredient_url'])
        print(sql)
        cursor.execute(sql)
        connection.commit()
