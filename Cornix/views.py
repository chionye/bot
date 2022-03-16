import requests,urllib
from .messages import *
from .Keyboards import *
import time,telebot,json
from telebot.types import *
from django.db.models import Q
from django.conf import settings
from ratelimiter import RateLimiter
from django.http import HttpResponse
from .txn_bot import check_transaction
from .models import User,MyOrder,MyClient,STEP
from django.views.decorators.http import require_http_methods


bot = telebot.TeleBot(settings.WEBHOOK_TOKEN,parse_mode='HTML') #Telegram Bot API
bot.enable_save_next_step_handlers(filename="handlers-saves/step.save",delay=2)


NEW_CLIENT = {}


def return_client_name(name):
	if "spot" in name or "linear" in name:
		return(True)
	else:
		return(False)


def user_details(message):
	detail = {}
	detail["chat_id"] = message.chat.id
	detail["msg_type"] = message.chat.type
	detail["user_id"] = message.from_user.id
	detail["username"] = message.from_user.username
	return(detail)


def return_exchange_and_step(userID):
	try:
		step = NEW_CLIENT[userID]["previuos_step"]
	except:
		step = "1"
	try:
		exchange = NEW_CLIENT[userID]["client_name"]
	except:
		try:
			exchange = NEW_CLIENT[userID]["exchange"]
		except:
			exchange = None

	return(step,exchange)


def validate_API_access(message):
	user_detail =  user_details(message)

	msg = client_creation_success_text.format(NEW_CLIENT[user_detail['user_id']]['client_name'])
	bot.send_message(user_detail["chat_id"],msg,reply_markup=client_creation_success())


def process_transaction_hash(message):
	user_detail =  user_details(message)

	msg = "Hello you transaction is being processed. Please wait"

	try:
		result = check_transaction(message.text,NEW_CLIENT[user_detail["chat_id"]]["deposit_amount"])

		if result == True:

			bot.send_message(user_detail["chat_id"],msg,reply_markup=ReplyKeyboardRemove(selective=False))#Main_Menu())
			bot.send_message(user_detail["chat_id"],"Once your deposit is confirmed the bot will start trading",reply_markup=Main_Menu())
			bot.clear_step_handler_by_chat_id(chat_id=user_detail["chat_id"])
		
		elif result == False:
			bot.send_message(user_detail["chat_id"],"There appears to be some incorrect details in your transaction.",reply_markup=ReplyKeyboardRemove(selective=False))
			bot.send_message(user_detail["chat_id"],"Please contact support to rectify this.",reply_markup=tech_support())
			
			bot.clear_step_handler_by_chat_id(chat_id=user_detail["chat_id"])
		else:
			msgs = bot.send_message(user_detail["chat_id"],"Invalid transaction hash, please check you transaction ID and try again")#Main_Menu())
			bot.register_next_step_handler(msgs,process_transaction_hash)

	except Exception as e:
		print(e)



def notify_admin(user):
	""" This is used to broadcast a new member subscription """
	admins = User.objects.filter(is_admin=True)
	user = User.objects.get(user_id=user)

	for admin in admins:

		if user.user_name == None:
			message_from = f"#{user.user_id}"
		else:
			message_from = f"@{user.user_name}"


		msg = f""" {message_from} started the bot for the first time
		"""
		bot.send_message(admin.chat_id,msg)


# CALLBACK QUERY HANDLING OCCURS HERE

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	print(call.data,"UHJIUGHHJKIIUHGJIUH")
	bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

	try:
		userID = call.from_user.id
		chat_id = call.message.chat.id
		user = User.objects.get(user_id=userID)

		try:
			NEW_CLIENT[userID]
		except KeyError:
			NEW_CLIENT[userID] = {}

		if call.data.endswith("@client"):
			q = call.data.split("@")[0]

			NEW_CLIENT[userID]["exchange"] = q
			NEW_CLIENT[userID]["previuos_step"] = "1"

			if q == "Binance" or q == "ByBit":
				bot.edit_message_text(chat_id=chat_id, text=step_1_2_of_3.format(q), message_id=call.message.message_id,reply_markup=new_client_step_1_2_of_3(q))
			else:
				bot.edit_message_text(chat_id=chat_id, text=step_2_of_3, message_id=call.message.message_id,reply_markup=new_client_step_2_of_3(q))

		elif call.data.startswith("option_"):
			NEW_CLIENT[userID]["previuos_step"] = "1_2"
			q = call.data.split(":")[1]
			option = call.data.split(":")[0].split("option_")[1]
			NEW_CLIENT[userID]["option"] = option.replace("_"," ").replace(q.lower(),"").title()

			if return_client_name(call.data) == False:
				q = option.replace("_","-").upper()
			else:
				pass

			bot.edit_message_text(chat_id=chat_id, text=step_2_of_3, message_id=call.message.message_id,reply_markup=new_client_step_2_of_3(q))

		elif call.data.startswith("set_name:"):
			q = call.data.split(":")[1]
			NEW_CLIENT[userID]["client_name"] = q
			NEW_CLIENT[userID]["previuos_step"] = "2"

			try:
				my_option = NEW_CLIENT[userID]["option"]
			except:
				my_option = ""

			bot.edit_message_text(chat_id=chat_id, text="Select the amount you want to deposit:", message_id=call.message.message_id,reply_markup=deposit_options())
			# msg = bot.edit_message_text(chat_id=chat_id, text=step_3_of_3.format(exchange=NEW_CLIENT[userID]["exchange"],option=my_option), message_id=call.message.message_id,reply_markup=new_client_step_3_of_3(q))
			# bot.register_next_step_handler(msg,validate_API_access)
			

		elif call.data.startswith("back_to_step:"):
			q = call.data.split(":")[1]

			step,exchange = return_exchange_and_step(userID)


			if q == "home":
				msg = """<b>Main Menu:</b>
				Choose an option"""
				bot.edit_message_text(chat_id=chat_id, text=msg, message_id=call.message.message_id,reply_markup=home_key())
			
			elif q == "about":
				bot.edit_message_text(chat_id=chat_id, text=about_cornix_auto, message_id=call.message.message_id,reply_markup=about_cornix(step))
			
			elif q == "my_portfolio":
				bot.edit_message_text(chat_id=chat_id, text=my_portfolio.format(0,0), message_id=call.message.message_id,reply_markup=my_portfolios_btn())

			elif q == "1":
				bot.edit_message_text(chat_id=chat_id, text=step_1_of_3, message_id=call.message.message_id,reply_markup=new_client_step_1_of_3())
			
			elif q == "2":
				bot.edit_message_text(chat_id=chat_id, text=step_2_of_3, message_id=call.message.message_id,reply_markup=new_client_step_2_of_3(exchange))

			elif q == "1_2":
				bot.edit_message_text(chat_id=chat_id, text=step_1_2_of_3.format(NEW_CLIENT[userID]["exchange"]), message_id=call.message.message_id,reply_markup=new_client_step_1_2_of_3(exchange))
			else:
				pass

		elif call.data.startswith("deposit:"):
			q = call.data.split(":")[1]
			NEW_CLIENT[userID]["deposit_amount"] = q

			detail = "<b>Please select your deposit currency:</b>"
			bot.edit_message_text(chat_id=chat_id, text=detail, message_id=call.message.message_id,reply_markup=payment_method())

		#THE BILLING PROGRAM STARTS HERE
		elif call.data.startswith("pay_with:"):
			q = call.data.split(":")[1]
			amount = NEW_CLIENT[userID]["deposit_amount"]
			if q == "UST":
				bot.answer_callback_query(call.id, "You are paying with UST")
				detail = payment_detail.format(amount,"UST",UST)
			else:
				bot.answer_callback_query(call.id, "You are paying with USDT")
				detail = payment_detail.format(amount,"USDT",USDT)
			bot.edit_message_text(chat_id=chat_id, text=detail, message_id=call.message.message_id,reply_markup=confirm_payment())

		elif call.data == "i_paid":
			user = User.objects.get(user_id=userID)

			detail = "Please send transaction ID/Hash as proof\nThis will be processed by the Bot Automatically"
			msgs = bot.send_message(chat_id=chat_id, text=detail,reply_markup=Cancel_btn())
			bot.register_next_step_handler(msgs,process_transaction_hash)

		# BOT CONFIGS
		elif call.data == "bot_configs":
			my_clients = []
			bot.edit_message_text(chat_id=chat_id, text=bot_config, message_id=call.message.message_id,reply_markup=bot_configs())
			
		elif call.data == "my_clients":
			my_clients = []
			bot.edit_message_text(chat_id=chat_id, text=client_config, message_id=call.message.message_id,reply_markup=bot_configs_clients(my_clients))

		elif call.data.startswith("my_client:"):
			q = call.data.split(":")[1]
			my_client = None # This is for a users client method
			bot.edit_message_text(chat_id=chat_id, text=configure_a_client, message_id=call.message.message_id,reply_markup=configs_clients(my_client))


		# MAIN MENU CALLBACK ACTION
		elif call.data == "return_to_menu":
			msg = """<b>Main Menu:</b>
			Choose an option"""
			bot.edit_message_text(chat_id=chat_id, text=msg, message_id=call.message.message_id,reply_markup=home_key())

		elif call.data == "my_portfolio":
			bot.edit_message_text(chat_id=chat_id, text=my_portfolio.format(0,0), message_id=call.message.message_id,reply_markup=my_portfolios_btn())

		elif call.data == "my_trades":
			bot.edit_message_text(chat_id=chat_id, text=trade_history, message_id=call.message.message_id,reply_markup=Main_Menu())

		elif call.data == "my_portfolio_faq":
			bot.edit_message_text(chat_id=chat_id, text=portfolio_info, message_id=call.message.message_id,reply_markup=my_portfolios_info_btn())

		elif call.data == "new_client":
			bot.edit_message_text(chat_id=chat_id, text=step_1_of_3, message_id=call.message.message_id,reply_markup=new_client_step_1_of_3())

		#ABOUT CORNIX CALLBACK DATA
		elif call.data == "about_cornix":
			bot.edit_message_text(chat_id=chat_id, text=about_cornix_auto, message_id=call.message.message_id,reply_markup=about_cornix())

		elif call.data == "about_cornix_E":
			bot.edit_message_text(chat_id=chat_id, text=about_cornix_E, message_id=call.message.message_id,reply_markup=about_cornix_back())

		elif call.data == "cornix_can_do":
			bot.edit_message_text(chat_id=chat_id, text=cornix_can_do, message_id=call.message.message_id,reply_markup=about_cornix_back())

		elif call.data == "made_for":
			bot.edit_message_text(chat_id=chat_id, text=made_for, message_id=call.message.message_id,reply_markup=about_cornix_back())

		elif call.data == "trade_for":
			bot.edit_message_text(chat_id=chat_id, text=trade_for, message_id=call.message.message_id,reply_markup=about_cornix_back())

		elif call.data == "cornix_features":
			bot.edit_message_text(chat_id=chat_id, text=cornix_features, message_id=call.message.message_id,reply_markup=about_cornix_back())

		else:
			pass
	except Exception as e:
		print(type(e).__name__,e,"CALLBACK ERROR")
		# bot.send_message(chat_id,step_1_of_3,reply_markup=new_client_step_1_of_3())



@bot.message_handler(commands=['start'])
def start(message):
	report = None
	user_detail = user_details(message)

	if user_detail["msg_type"] == "private":
		try:
			user = User.objects.get(user_id=user_detail["user_id"])
		except User.DoesNotExist:
			user = User(user_name=user_detail["username"],chat_id=user_detail["chat_id"],user_id=user_detail["user_id"])
			user.save()

		try:
			NEW_CLIENT[user_detail["user_id"]]
		except KeyError:
			NEW_CLIENT[user_detail["user_id"]] = {}

		bot.send_message(user_detail["chat_id"],step_1_of_3,reply_markup=new_client_step_1_of_3())
	else:
		pass

	
@bot.message_handler(content_types=['text'])
def reply_msg(message):
	user_detail = user_details(message)
	user = User.objects.get(user_id=user_detail['user_id'])
	
	if user_detail["msg_type"] == "private":

		bot.send_message(user_detail["chat_id"],message.text)


	else:
		pass


@require_http_methods(["GET","POST"])
# @RateLimiter(max_calls=100, period=1)
def WebConnect(request):
	# Listens only for GET and POST requests
	# returns django.http.HttpResponseNotAllowed for other requests
	# Handle the event appropriately

	if request.method == 'POST':
		jsondata = request.body
		data = json.loads(jsondata)
		update = telebot.types.Update.de_json(data)
		bot.process_new_updates([update])
		return HttpResponse(status=201)
	else:
		bot.remove_webhook()
		bot.set_webhook(url=settings.WEBHOOK_URL+settings.WEBHOOK_TOKEN)
		return HttpResponse(status=201)


bot.load_next_step_handlers(filename="handlers-saves/step.save")
