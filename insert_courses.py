import config
import sqlite3
from moodleapi import Moodle
# from course import Course

api = Moodle(url=config.url, token=config.moodle_token)
data = ((course['id'], course['fullname']) for course in api.courses)

query = 'insert into courses (moodle_id, name) values (?, ?)'

connection = sqlite3.connect('database/pedcoter.db')
cursor = connection.cursor()
cursor.executemany(query, data)

connection.commit()
connection.close()
