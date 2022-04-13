# from .models import Subcriptions
from datetime import datetime, timedelta
from dateutil.relativedelta import *


USDT = "TTLt2GSvrZy4dLHUJJFgiAMekHoKBj2VYr"
ETH = "0x675d8013F48D6917a5F0C5245616c8AdEBeEBA63"
BTC = "1hc1GexRFmRVcpfhRZzuSwjvWYdkDjC2s"
TRX = "TTLt2GSvrZy4dLHUJJFgiAMekHoKBj2VYr"
DOT = "13eQZMvLexfBZJUD5jnCjBaBLnkEaFTFyG6ofb2GVvgtDdP7"

XRP = "r9beU5KAbECKKdnaAbNLGWsAJZvFgaHZyV"
DODGE = "DFTkqh852yyF8awffVXvbQqDxYzC1eUitk"

SOL = "CAED2xivAPQFEbPP52hT28v5zUceyswADC8i7fS2WGaZ"


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
