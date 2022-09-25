import config
from bot import TelegramBot
from moodleapi import Moodle
from csv import DictWriter
from resource import Resource
import time

def read_ref(filename):
    with open(filename, 'r') as file:
        ref = int(file.read())
    return ref

def write_ref(filename, ref):
    with open(filename, 'w') as file:
        file.write(str(ref))

api = Moodle(url=config.url, token=config.moodle_token)
course = api.courses[1]
bot = TelegramBot(config.telegram_token, config.chat_id)

filename = 'ref.txt'

new_timemodified = 0
i = 0

while True:
    print('consulta', i)
    response = api.resources_by_course(course)
    ref_timemodified = read_ref(filename)
    for resource in response['resources']:
        resource = Resource(resource)
        if resource.timemodified > ref_timemodified:
            bot.send_resource(resource)
            time.sleep(3)
            if resource.timemodified > new_timemodified:
                new_timemodified = resource.timemodified
    time.sleep(config.timeout)
    if new_timemodified > ref_timemodified:
        write_ref(filename, new_timemodified)
    i += 1

