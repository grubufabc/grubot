import logging
import json
from duel import *
from cf2 import * 
from datetime import datetime
from telegram.ext import (Updater, CommandHandler, MessageHandler, 
                          ConversationHandler, Filters, PicklePersistence)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

LINK = range(1)

def duel (update, context):
	duel_handles = context.args
	context.user_data['duel_handles'] = duel_handles
	update.message.reply_text('Handles registradas! \nEnviar /link seguido do link do problema.'
	                          '\nOu enviar /cancelar para cancelar o duelo.'
	)
	
	return LINK

def link (update, context):
	link = context.args[0]
	context.user_data['link'] = link
	duel_handles = context.user_data['duel_handles']
	context.bot.send_message(chat_id = update.effective_chat.id, text = 'Duelo entre ' + duel_handles[0] + 
	                                                                    ' e ' + duel_handles[1] + "!")
	d = Duel(duel_handles, link)
	d.start()

	context.user_data['duel_handles'].clear()
	context.user_data['link'] = ""
	return ConversationHandler.END

def cancel (update, context):
	user = update.message.from_user
	update.message.reply_text("O duelo foi cancelado!")	

	context.user_data['duel_handles'].clear()
	context.user_data['link'] = ""
	return ConversationHandler.END

# /rating "sua_handle"
# Retorna a rating da handle digitada no codeforces
def rating (update, context):
	handle = context.args[0]
	user_rating = User(handle).getUserRating()
	update.message.reply_text("Rating de " + handle + ": " + str(user_rating))

# /add_handle "sua_handle"
# Adiciona sua handle e rating ao arquivo datagrubot
def add_handle (update, context): # pode ser editada para adicionar mais informações ao usuário
	handle = context.args[0]
	rating = User(handle).getUserRating()

	if checkFieldInArray(context.user_data, "user_handles") is False:
		context.user_data['user_handles'] = []
		
	context.user_data['user_handles'].append({handle: rating})

# /ratings
# retorna as ratings das handles presentes no arquivo datagrubot
def ratings (update, context):
	ratings = "Ratings:\n\n"

	for user in context.user_data['user_handles']:
		keys = user.keys()
		for key in keys:
			ratings += '{} - {}\n'.format(key, user[key])

	update.message.reply_text(ratings)

# /upcoming
# Retorna os próximos rounds (ranqueados)? do codeforces
def upcoming (update, context):
	upcoming = ""
	contests = CFWatcher().getNextContests()
	
	contests.sort(key = lambda contest: contest['startTimeSeconds'])

	for contest in contests:
		upcoming += '{} ({})\n'.format(
			contest['name'], 
			getFormattedTime(contest['durationSeconds'])
		)
		constestStart = contest['startTimeSeconds']
		now = datetime.timestamp(datetime.now())
		upcoming += 'Começa em: {}\n\n'.format(getFormattedTime(constestStart - now))

	update.message.reply_text(upcoming)

# /show_data
# Retorna os dados que o bot armazenou
def show_data(update, context):
	update.message.reply_text("This is what you already told me:"
							  "{}".format(facts_to_str(context.user_data)))

def facts_to_str(user_data):
	facts = list()

	for key, value in user_data.items():
		facts.append('{} - {}'.format(key, value))

	return "\n".join(facts).join(['\n', '\n'])

def checkFieldInArray (array, field):
	for i in array:
		if i == field:
			return True
	return False	

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

	user_rating_handler = CommandHandler('rating', rating)
	dispatcher.add_handler(user_rating_handler)

	ratings_handler = CommandHandler('ratings', ratings)
	dispatcher.add_handler(ratings_handler)

	upcoming_handler = CommandHandler('upcoming', upcoming)
	dispatcher.add_handler(upcoming_handler)

	add_handle_handler = CommandHandler('add_handle', add_handle)
	dispatcher.add_handler(add_handle_handler)

	show_data_handler = CommandHandler('show_data', show_data)
	dispatcher.add_handler(show_data_handler)

	# Inicia o bot
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
