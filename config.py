from decouple import config as getenv
url = getenv('URL')
moodle_token = getenv('MOODLE_TOKEN')
telegram_token = getenv('TELEGRAM_TOKEN')
chat_id = getenv('CHAT_ID')
timeout = getenv('TIMEOUT', cast=int)

