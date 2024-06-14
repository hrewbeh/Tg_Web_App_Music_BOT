import os
import time
import asyncio
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes, filters, ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler

load_dotenv()
TOKEN = os.getenv('TOKEN')

NAME, PASSWORD, EMAIL, END = range(4)  # Это для регистрации
NAME2, PASSWORD2, END2 = range(3)  # Для входа
SONG = range(1)

API_URL = 'http://127.0.0.1:8000/registration'
API_URL_DELETE_MUSE = 'http://127.0.0.1:8000/delete_music'
API_URL_LOGIN = 'http://127.0.0.1:8000/login'
API_URL_DELETE = 'http://127.0.0.1:8000/delete'

API_URL_DOWNLOAD_MUSIC = 'http://127.0.0.1:8000/download'
QUERY = range(1)

COUNT = 0  # Означает вошел ли пользователь


def check_muse(tg_id):
	pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	id = update.message.chat_id  # Тут мы определяем айди
	await context.bot.send_message(chat_id=id, text='соси')


async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if COUNT == 1:
		message = await context.bot.send_message(chat_id=update.message.chat_id, text='Че ищем')
		context.user_data['bot_message'] = message.message_id
		return QUERY
	elif COUNT == 0:
		message2 = await context.bot.send_message(chat_id=update.message.chat_id, text='Вы не вошли')
		context.user_data['bot_message'] = message2.message_id
		await asyncio.sleep(5)
		await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])


async def query(update: Update, context: ContextTypes.DEFAULT_TYPE):
	query = update.message.text
	id = update.message.chat_id
	async with aiohttp.ClientSession() as session:
		async with session.post(API_URL_DOWNLOAD_MUSIC,
		                        data={'query': str(query), 'tg_id': str(id)}) as rest:
			if rest.status == 200:
				file_path = await rest.text()
				file_path = file_path.strip()  # Удалить возможные пробелы
				await context.bot.send_message(chat_id=update.message.chat_id, text='Файл загружен')
				await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
				await context.bot.delete_message(chat_id=update.message.chat_id,
				                                 message_id=context.user_data['bot_message'])
				
				with open(f'media/{id}/{file_path}', 'rb') as audio:
					await context.bot.send_audio(chat_id=update.message.chat_id, audio=audio)
			else:
				await context.bot.send_message(chat_id=update.message.chat_id, text='пошел нахер')
	return ConversationHandler.END


async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if COUNT == 1:
		message = await context.bot.send_message(chat_id=update.message.chat_id, text='Че удаляем?')
		context.user_data['bot_message'] = message.message_id
		return SONG
	elif COUNT == 0:
		message2 = await context.bot.send_message(chat_id=update.message.chat_id, text='Вы не вошли')
		context.user_data['bot_message'] = message2.message_id
		time.sleep(5)
		await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])


async def delete_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
	query = update.message.text
	async with aiohttp.ClientSession() as session:
		async with session.post(API_URL_DELETE_MUSE,
		                        data={'query': query, 'tg_id': update.message.chat_id}) as rest:
			if rest.status == 200:
				await context.bot.send_message(chat_id=update.message.chat_id, text='Послушный мальчик')
				await context.bot.delete_message(chat_id=update.message.chat_id,
				                                 message_id=update.message.message_id)
				
				await context.bot.delete_message(chat_id=update.message.chat_id,
				                                 message_id=context.user_data['bot_message'])
			else:
				await context.bot.send_message(chat_id=update.message.chat_id,
				                               text='пошел нахер')
	return ConversationHandler.END


# Блок регистрации сделать на Конверсэйшн

async def pes(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message = await context.bot.send_message(chat_id=update.message.chat_id, text='Your Name')
	context.user_data['bot_message'] = message.message_id
	return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data['name'] = update.message.text
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	message = await context.bot.send_message(chat_id=update.message.chat_id, text='Your password')
	context.user_data['bot_message'] = message.message_id
	
	return PASSWORD


async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data['password'] = update.message.text
	
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	message = await context.bot.send_message(chat_id=update.message.chat_id, text='Your email')
	context.user_data['bot_message'] = message.message_id
	
	return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data['email'] = update.message.text
	emaill = context.user_data['email']
	tg_id = update.message.chat_id
	name = context.user_data['name']
	password = context.user_data['password']
	
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	message = await context.bot.send_message(chat_id=update.message.chat_id,
	                                         text=f'Подтвердите данные\n{name}\n{password}\n{emaill}\n{tg_id}')
	await context.bot.send_message(chat_id=update.message.chat_id, text=f'Нажми "Y" если все ок')
	context.user_data['bot_message'] = message.message_id
	
	return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
	emaill = context.user_data['email']
	tg_id = update.message.chat_id
	name = context.user_data['name']
	password = context.user_data['password']
	user_lox = update.message.text
	
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	if user_lox.lower() == 'y':
		async with aiohttp.ClientSession() as session:
			async with session.post(API_URL,
			                        data={'tg_id': tg_id, 'name': name, 'password': password, 'email': emaill}) as rest:
				if rest.status == 200:
					global COUNT
					COUNT = 1
					await context.bot.send_message(chat_id=update.message.chat_id, text='Послушный мальчик')
				elif rest.status == 400:
					await context.bot.send_message(chat_id=update.message.chat_id, text='Пользователь уже существует')
				else:
					await context.bot.send_message(chat_id=update.message.chat_id,
					                               text='Произошла ошибка сервера но регистрация прошла успешно, так что пошел нахер')
		return ConversationHandler.END
	else:
		await context.bot.send_message(chat_id=update.message.chat_id, text='Дэбил')
		return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(chat_id=update.message.chat_id, text='Регистрация отменена.')
	return ConversationHandler.END


# end

async def pes2(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message = await context.bot.send_message(chat_id=update.message.chat_id, text='Your Name')
	context.user_data['bot_message'] = message.message_id
	return NAME2


async def name2(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data['name'] = update.message.text
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	message = await context.bot.send_message(chat_id=update.message.chat_id, text='Your password')
	context.user_data['bot_message'] = message.message_id
	
	return PASSWORD2


async def password2(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data['password'] = update.message.text
	
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	message = await context.bot.send_message(chat_id=update.message.chat_id, text='Нажми "Y" если все окl')
	context.user_data['bot_message'] = message.message_id
	
	return END2


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
	name = context.user_data['name']
	password = context.user_data['password']
	user_lox = update.message.text
	
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['bot_message'])
	await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
	
	if user_lox.lower() == 'y':
		async with aiohttp.ClientSession() as session:
			async with session.post(API_URL_LOGIN,
			                        data={'name': name, 'password': password}) as rest:
				if rest.status == 200:
					global COUNT
					COUNT = 1
					await context.bot.send_message(chat_id=update.message.chat_id, text='Послушный мальчик\nТы вошел')
				else:
					await context.bot.send_message(chat_id=update.message.chat_id,
					                               text='пошел нахер')
		return ConversationHandler.END
	else:
		await context.bot.send_message(chat_id=update.message.chat_id, text='Дэбил')
		return ConversationHandler.END


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global COUNT
	COUNT = 1
	await context.bot.send_message(chat_id=update.message.chat_id, text='Вы вышли')


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
	async with aiohttp.ClientSession() as session:
		async with session.post(API_URL_DELETE,
		                        data={'tg_id': update.message.chat_id}) as rest:
			if rest.status == 200:
				global COUNT
				COUNT = 0
				await context.bot.send_message(chat_id=update.message.chat_id, text='Послушный мальчик\nТы вышел')
			elif rest.status == 404:
				await context.bot.send_message(chat_id=update.message.chat_id, text='Пользователь не существует')
			else:
				await context.bot.send_message(chat_id=update.message.chat_id,
				                               text='пошел нахер')


def run_bot():
	application = ApplicationBuilder().token(TOKEN).build()
	application.add_handler(CommandHandler('start', start))
	application.add_handler(CommandHandler('muse', download_music))
	application.add_handler(CommandHandler('logout', logout))
	application.add_handler(CommandHandler('delete', delete_user))
	application.add_handler(ConversationHandler(
		entry_points=[CommandHandler('registration', pes)],
		states={
			NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name), ],
			PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password), ],
			EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email), ],
			END: [MessageHandler(filters.TEXT & ~filters.COMMAND, end), ],
		},
		fallbacks=[CommandHandler('cancel', cancel)],
	))
	application.add_handler(ConversationHandler(
		entry_points=[CommandHandler('login', pes2)],
		states={
			NAME2: [MessageHandler(filters.TEXT & ~filters.COMMAND, name2), ],
			PASSWORD2: [MessageHandler(filters.TEXT & ~filters.COMMAND, password2), ],
			END2: [MessageHandler(filters.TEXT & ~filters.COMMAND, login), ],
		},
		fallbacks=[CommandHandler('cancel', cancel)],
	))
	application.add_handler(ConversationHandler(
		entry_points=[CommandHandler('delete_music', song)],
		states={
			SONG: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_music), ]
		},
		fallbacks=[CommandHandler('cancel', cancel)],
	))
	application.add_handler(ConversationHandler(
		entry_points=[CommandHandler('download_music', download_music)],
		states={
			QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, query), ]
		},
		fallbacks=[CommandHandler('cancel', cancel)],
	))
	application.run_polling()
