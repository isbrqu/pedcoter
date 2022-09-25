import config
from bot import TelegramBot
from moodleapi import Moodle
from csv import DictWriter
from resource import Resource
import time

api = Moodle(url=config.url, token=config.moodle_token)
course = api.courses[0]
bot = TelegramBot(config.telegram_token, config.chat_id)

ref_timemodified = 0
new_timemodified = 0
i = 0

while True:
    print('consulta', i)
    response = api.resources_by_course(course)
    for resource in response['resources']:
        resource = Resource(resource)
        if resource.timemodified > ref_timemodified:
            bot.send_resource(resource)
            time.sleep(3)
            if resource.timemodified > new_timemodified:
                new_timemodified = resource.timemodified
    time.sleep(config.timeout)
    if new_timemodified > ref_timemodified:
        ref_timemodified = new_timemodified
    i += 1

