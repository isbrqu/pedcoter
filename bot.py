import requests

API_URL = "https://api.telegram.org"

class TelegramBot(object):

    def __init__(self, token, chat_id):
        self.url = API_URL + '/bot' + token + '/sendMessage'
        self.data = {'chat_id': chat_id}

    def send_resource(self, resource):
        self.data['text'] = resource.as_message
        response = requests.post(self.url, data=self.data).json()
        return response
    
