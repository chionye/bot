# from .models import Subcriptions
from datetime import datetime, timedelta
from dateutil.relativedelta import *


USDT = "TJLtLvqRvPbYZPRDQPxSpFruCCXRXSSci3"
UST = "terra1d3gld968chca9val3dek7y8msyr9ph2fkqhced"


PLAN = {
	"1_MONTH":"$1000",
	"3_MONTH":"$3000",
	"6_MONTH":"$6000",
	"12_MONTH":"$12000",
	"_MONTH":"$20000",
}

PLAN_CHOICE = {
	"1_MONTH":"1_MONTH",
	"3_MONTH":"3_MONTH",
	"6_MONTH":"6_MONTH",
	"12_MONTH":"12_MONTH",
	"_MONTH":"LIFETIME",
}

PLAN_Benefit = {
	"1_MONTH":"Earn 2x of your portfoilio in a month trading with this plan",
	"3_MONTH":"Earn 5x of your portfolio with this plan\n Using this plan the bot maximizes your profits",
	"6_MONTH":"Earn 10x or more of your portfolio trading with this plan\n Using this plan the bot maximizes your profits\nwith this plan there is more risk managament involved",
	"12_MONTH":"Earn 10x or more of your portfolio trading with this plan\n Using this plan the bot maximizes your profits\nwith this plan there is proper risk managament involved",
	"_MONTH":"Earn 10x or more of your portfolio trading with this plan\n Using this plan the bot maximizes your profits\nwith this plan there is proper risk managament involved and guess what, this is a lifetime plan no more subscriptions",
}



def get_plan(plan):
	if plan == '1_month':
		return(PLAN['1_MONTH'])
	elif plan == '3_months':
		return(PLAN['3_MONTH'])
	elif plan == '6_months':
		return(PLAN['6_MONTH'])
	elif plan == '1_year':
		return(PLAN['12_MONTH'])
	elif plan == '_year':
		return(PLAN['_MONTH'])
	else:
		return(None)


def get_benefits(plan):
	if plan == '1_month':
		return(PLAN_Benefit['1_MONTH'])
	elif plan == '3_months':
		return(PLAN_Benefit['3_MONTH'])
	elif plan == '6_months':
		return(PLAN_Benefit['6_MONTH'])
	elif plan == '1_year':
		return(PLAN_Benefit['12_MONTH'])
	elif plan == '_year':
		return(PLAN_Benefit['_MONTH'])
	else:
		pass

def selected_plan(plan):
	if plan == '1_month':
		return(PLAN_CHOICE['1_MONTH'])
	elif plan == '3_months':
		return(PLAN_CHOICE['3_MONTH'])
	elif plan == '6_months':
		return(PLAN_CHOICE['6_MONTH'])
	elif plan == '1_year':
		return(PLAN_CHOICE['12_MONTH'])
	elif plan == '_year':
		return(PLAN_CHOICE['_MONTH'])
	else:
		pass


def return_end_date(plan):
	date = datetime.utcnow().replace(tzinfo=None)

	if plan == '1_month':
		return(date + relativedelta(months=+1))
	elif plan == '3_months':
		return(date + relativedelta(months=+3))
	elif plan == '6_months':
		return(date + relativedelta(months=+6))
	elif plan == '1_year':
		return(date + relativedelta(months=+12))
	elif plan == '_year':
		return(date + relativedelta(months=+10000))
	else:
		pass


def is_active(user):
	try:
		sub = Subcriptions.objects.get(subscriber=user)
		if sub.active == True:
			if (sub.date_expired.replace(tzinfo=None) - datetime.utcnow().replace(tzinfo=None)) < timedelta(1):
				# Check if the user's subscription has expired
				Subcriptions.objects.filter(subscriber=user).update(active = False,paid=False)
				return(False)
			else:
				return(True)
			return
		else:
			return(False)
	except Subcriptions.DoesNotExist:
		return(False)
