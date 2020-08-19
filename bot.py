import logging
import json
from duel import *
from cf2 import * 
from telegram.ext import (Updater, CommandHandler, MessageHandler, 
                          ConversationHandler, Filters, PicklePersistence)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level = logging.INFO)

logger = logging.getLogger(__name__)

LINK = range(1)

def duel (update, context):
	handles = context.args
	context.user_data['handles'] = handles
	update.message.reply_text('Handles registradas! \nEnviar /link seguido do link do problema.'
	                          '\nOu enviar /cancelar para cancelar o duelo.'
	)
	
	return LINK

def link (update, context):
	link = context.args[0]
	context.user_data['link'] = link
	handles = context.user_data['handles']
	context.bot.send_message(chat_id = update.effective_chat.id, text = 'Duelo entre ' + handles[0] + 
	                                                                    ' e ' + handles[1] + "!")
	d = Duel(handles, link)
	d.start()

	context.user_data['handles'] = "" #isso está porco
	context.user_data['link'] = ""
	return ConversationHandler.END

def cancel (update, context):
	user = update.message.from_user
	update.message.reply_text("O duelo foi cancelado!")	

	context.user_data['handles'] = "" #isso está porco
	context.user_data['link'] = ""
	return ConversationHandler.END

def rating (update, context):
	handle = context.args[0]
	user_rating = User(handle).getUserRating()
	update.message.reply_text("Toma-lhe rating: " + str(user_rating))

def facts_to_str(user_data):
	facts = list()

	for key, value in user_data.items():
		facts.append('{} - {}'.format(key, value))

	return "\n".join(facts).join(['\n', '\n'])

def show_data(update, context):
	update.message.reply_text("This is what you already told me:"
							  "{}".format(facts_to_str(context.user_data)))

def main ():

	pp = PicklePersistence(filename = "datagrubot")
	token = "1200519958:AAEsmRay1p5RZJWa9wjIEt9cqD-b2MNKtvg"
	updater = Updater(token = token, persistence = pp, use_context = True)

	dispatcher = updater.dispatcher

	# Handlers

	duel_handler = ConversationHandler(
		entry_points = [CommandHandler('duelo', duel)],

		states = {
			LINK: [CommandHandler('link', link)]
		},

		fallbacks = [CommandHandler('cancelar', cancel)],
		name = "duel",
		persistent = True
	)
	dispatcher.add_handler(duel_handler)

	user_rating = CommandHandler('rating', rating)
	dispatcher.add_handler(user_rating)

	show_data_handler = CommandHandler('show_data', show_data)
	dispatcher.add_handler(show_data_handler)

	# Start the bot
	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
