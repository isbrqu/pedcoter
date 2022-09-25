import telegram
import config

def main():
    bot = telegram.Bot(config.telegram_token)
    for update in bot.get_updates():
        message = update.message
        print(message.chat.id, message.text)
    # update = bot.get_updates()[0]
    # chat = update.message.chat
    # bot.send_message(chat.id, 'hola')
    

if __name__ == '__main__':
    main()
