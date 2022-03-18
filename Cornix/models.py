import uuid
from django.db import models
from django.urls import reverse
from datetime import datetime




class User(models.Model):
	"""
		The model holding all our telegram users
	"""
	chat_id = models.CharField(max_length=120,null=True,blank=False)
	user_name = models.CharField(max_length=120,null=True,blank=True,editable=False)
	user_id = models.CharField(primary_key=True,max_length=120, null=False, blank=False,editable=False)
	is_admin = models.BooleanField(default=False) # Used to denote a user who is an admin
	date_joined = models.DateTimeField(auto_now_add=True,null=False,editable=False)#date user started using the bot
	holding = models.BooleanField(default=False) # Used to denote a user is in a buying order if True else the user is in selling mode
	def __str__(self):
		return(str(self.user_id))




class MyClient(models.Model):
	"""
	Model re-presenting a user'r client
	"""

	client_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False, unique=True)
	client_name =   models.CharField(max_length=120,blank=True)# The clients name given by the user
	myclient = models.ForeignKey(User, on_delete=models.CASCADE,editable=False) # The user who owns this client
	balance = models.FloatField(default=0.0) #USDT balance
	has_funds = models.BooleanField(default=False) # Used to denote a user who has deposited funds
	start_trading = models.BooleanField(default=False) # Used to signify that this client is ready to start trading
	initial_deposit_date = models.DateTimeField(auto_now_add=True, null=False)# date this client was created
	exchange =   models.CharField(max_length=20,)# The exchange the bot is to trade in
	

	def __str__(self):
		return(str(self.client_id))


class MyOrder(models.Model):
	"""
	Model re-presenting all transaction orders
	 executed/submitted by a user
	"""
	BUY = "buy"
	SELL = "sell"
			
	ORDER_LIST = [
		(BUY, 'Buy'),
		(SELL, 'Sell'),]
	
	
	order_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False, unique=True)
	client = models.ForeignKey(MyClient, on_delete=models.CASCADE,editable=False) # The Client the bot is making the order for
	coin_pair =   models.CharField(max_length=20,)# Example is BTC/USDT or ETH/USDT
	order_type =  models.CharField(max_length=4,choices=ORDER_LIST,default=BUY,)#multichoice buy/sell
	amount = models.FloatField(default=0.0)
	date_placed = models.DateTimeField(auto_now_add=True, null=False)# date transaction was submitted


	
	def __str__(self):
		return(str(self.order_id))


class STEP(models.Model):
	"""
	Model re-presenting a user'r client
	"""

	step_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False, unique=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE,editable=False) # The user who owns this client
	next_step = models.CharField(max_length=20,)# The current step the use is in
	state = models.TextField(blank = True)

	def __str__(self):
		return(str(self.step_id))




