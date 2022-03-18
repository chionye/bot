from django.contrib import admin
from .models import User,MyOrder,MyClient,STEP




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('user_id','user_name',)
	list_display = ['user_id','user_name','is_admin','date_joined',]


@admin.register(MyOrder)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('order_id','client',)
	list_display = ['order_id','client','coin_pair','order_type','date_placed']


@admin.register(MyClient)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('client_id','myclient',)
	list_display = ['client_id','myclient','exchange','balance','has_funds','start_trading','initial_deposit_date']


@admin.register(STEP)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('step_id','user',)
	list_display = ['step_id','user','next_step','state',]

