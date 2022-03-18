# from .models import Subcriptions
from datetime import datetime, timedelta
from dateutil.relativedelta import *


USDT = "TTLt2GSvrZy4dLHUJJFgiAMekHoKBj2VYr"
UST = "terra1d3gld968chca9val3dek7y8msyr9ph2fkqhced"



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
