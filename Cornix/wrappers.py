import requests
import http.client
from config import *
from tronapi import Tron
from tronapi import HttpProvider

full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')
tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)



def check_usdt_transaction(hash):
	try:
		result = tron.trx.get_transaction(hash)
		status = result["ret"][0]['contractRet']
		result = result['raw_data']['contract'][0]['parameter']['value']
		amount = float(result['amount']/1000000)
		to_address = tron.address.from_hex(result['to_address']).decode('ascii')


		if status == "SUCCESS" and to_address == USDT:
			return(True)
		else:
			return(False)

	except Exception as e:
		if "INVALID hex String" in str(e):
			return("Invalid transaction hash")


def check_sol_txn(hashx):
	decimal = 1000000000
	base_url = f"https://public-api.solscan.io/transaction/{hashx}"

	try:
		data = requests.get(base_url).json()
		status = data["status"]

		from_wallet = data["parsedInstruction"][1]["params"]["source"]
		amount = int(data["parsedInstruction"][1]["params"]["amount"])/decimal

		if status == "Success":# and from_wallet == SOL:
			return(True,amount)
		else:
			return(False,None)
	except Exception as e:
		print(e)
		return(False,None)


def check_eth_txn(hashx):
	apikey = "D31TRVDJRHCIKKCXGE43EV37M3Z8W6UI96"
	base_url = f"https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash={hashx}&apikey={apikey}"

	try:
		data = requests.get(base_url).json()
		status = int(data["result"]['status'])

		if status == 1:
			return(True)
		else:
			return(False)
	except Exception as e:
		print(e)
		return(False)





def check_xrp_txn(hashx):
	# conn = http.client.HTTPConnection("https://rest.cryptoapis.io/v2")
	# querystring = {"context":"yourExampleString"}
	headers = {
	  'Content-Type': "application/json",
	  'X-API-Key': "ee6a268f304c5f76ae8bbd5ad9d031df41cc8432"
	}


	base_url = "https://rest.cryptoapis.io/v2/blockchain-data/xrp-specific/mainnet/transactions/{hashx}?context=yourExampleString"
	data = requests.get(base_url,headers=headers).json()
	return(data)

hashx = "0F8FA9A43F96527FC599FEC7E2B0C99FE31503C187C473181C90CBDB900D82DD"
# print(check_xrp_txn(hashx))