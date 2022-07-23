import os
from dotenv import load_dotenv
from ngrok_utils import NgrokWraper
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

load_dotenv()

class bot:
    def __init__(self):
        self.ngrok_client = NgrokWraper(os.getenv('NGROK'))

    def start(self, update, context):
        print('test')

    def temp(self, update, context):
        ''' TEMP '''
        # Enviar un mensaje a un ID determinado.
        temp = os.popen('sensors | grep \"temp\" | awk -F\"+\" \'{print $2}\'').read()
        #self.client.send_message(f"Temperatura: {temp}")
        context.bot.send_message(update.message.chat_id, f'Temperatura: {temp}')

    def ngrok(self, update, context):
        msg = self.ngrok_client.get_online_tunnels()
        context.bot.send_message(update.message.chat_id, msg)

    def unknown(self, update, context):
        update.message.reply_text("De que monda me estas hablando perra malparida.")

    def run(self):
        updater=Updater(os.getenv('TOKEN'), use_context=True)
        dp=updater.dispatcher

        dp.add_handler(CommandHandler('start',self.start))
        dp.add_handler(CommandHandler('temp',self.temp))
        dp.add_handler(CommandHandler('ngrok',self.ngrok))
        dp.add_handler(MessageHandler(Filters.text,self.unknown))

        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
    bot = bot()
    bot.run()
