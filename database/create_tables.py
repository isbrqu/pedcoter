import sqlite3

connection = sqlite3.connect('pedcoter.db')
cursor = connection.cursor()

tables = (
    'courses',
    'types',
    'resources',
)

for table in tables:
    with open('table_' + table + '.sql', 'r') as file:
        query = file.read()
        cursor.execute(query)

connection.commit()
connection.close()
