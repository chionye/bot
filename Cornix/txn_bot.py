from .config import *
from tronapi import Tron
from tronapi import HttpProvider

full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')
tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)


def check_transaction(hash,sent_amount):
	try:
		result = tron.trx.get_transaction(hash)
		status = result["ret"][0]['contractRet']
		result = result['raw_data']['contract'][0]['parameter']['value']
		amount = float(result['amount']/1000000)
		to_address = result['to_address']

		print(status)
		print(amount)
		print(to_address)

		if status == "SUCCESS" and to_address == USDT and amount == float(sent_amount):
			return(True)
		else:
			return(False)

	except Exception as e:
		if "INVALID hex String" in str(e):
			return("Invalid transaction hash")


# hashx = "de2eac588cca0e623cbe18fbc64ad4f1de388646a075a2bd7f25c05a983d1da4"
# sent_amount = 2163.175
# print(check_transaction(hashx,sent_amount))