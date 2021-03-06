# from lib.openfood_env import MULTI_1X
# from lib.openfood_env import MULTI_2X
# from lib.openfood_env import MULTI_3X
# from lib.openfood_env import MULTI_4X
# from lib.openfood_env import MULTI_5X
from lib.openfood_env import KOMODO_NODE
from lib.openfood_env import RPC_USER
from lib.openfood_env import RPC_PASSWORD
from lib.openfood_env import RPC_PORT
from lib.openfood_env import KV1_NODE
from lib.openfood_env import KV1_RPC_USER
from lib.openfood_env import KV1_RPC_PASSWORD
from lib.openfood_env import KV1_RPC_PORT
from lib.openfood_env import EXPLORER_URL
from lib.openfood_env import THIS_NODE_RADDRESS
from lib.openfood_env import THIS_NODE_WIF
from lib.openfood_env import BLOCKNOTIFY_CHAINSYNC_LIMIT
from lib.openfood_env import HOUSEKEEPING_RADDRESS
from lib.openfood_env import IMPORT_API_BASE_URL
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.openfood_env import openfood_API_BASE_URL
from lib.openfood_env import openfood_API_ORGANIZATION
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE
from lib.openfood_env import openfood_API_ORGANIZATION_BATCH
from lib.openfood_env import FUNDING_AMOUNT_CERTIFICATE
from lib.openfood_env import FUNDING_AMOUNT_TIMESTAMPING_START
from lib.openfood_env import FUNDING_AMOUNT_TIMESTAMPING_END
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_PATH
from lib.openfood_env import WALLET_DELIVERY_DATE
from lib.openfood_env import WALLET_DELIVERY_DATE_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_DELIVERY_DATE_THRESHOLD_UTXO
from lib.openfood_env import WALLET_DELIVERY_DATE_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_PON
from lib.openfood_env import WALLET_PON_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_PON_THRESHOLD_UTXO
from lib.openfood_env import WALLET_PON_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_MASS_BALANCE
from lib.openfood_env import WALLET_MASS_BALANCE_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_MASS_BALANCE_THRESHOLD_UTXO
from lib.openfood_env import WALLET_MASS_BALANCE_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_TIN
from lib.openfood_env import WALLET_TIN_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_TIN_THRESHOLD_UTXO
from lib.openfood_env import WALLET_TIN_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_PROD_DATE
from lib.openfood_env import WALLET_PROD_DATE_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_PROD_DATE_THRESHOLD_UTXO
from lib.openfood_env import WALLET_PROD_DATE_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_JULIAN_START
from lib.openfood_env import WALLET_JULIAN_START_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_JULIAN_START_THRESHOLD_UTXO
from lib.openfood_env import WALLET_JULIAN_START_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_JULIAN_STOP
from lib.openfood_env import WALLET_JULIAN_STOP_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_JULIAN_STOP_THRESHOLD_UTXO
from lib.openfood_env import WALLET_JULIAN_STOP_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_BB_DATE
from lib.openfood_env import WALLET_BB_DATE_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_BB_DATE_THRESHOLD_UTXO
from lib.openfood_env import WALLET_BB_DATE_THRESHOLD_UTXO_VALUE
from lib.openfood_env import WALLET_ORIGIN_COUNTRY
from lib.openfood_env import WALLET_ORIGIN_COUNTRY_THRESHOLD_BALANCE
from lib.openfood_env import WALLET_ORIGIN_COUNTRY_THRESHOLD_UTXO
from lib.openfood_env import WALLET_ORIGIN_COUNTRY_THRESHOLD_UTXO_VALUE
from lib.openfood_env import KV1_ORG_POOL_WALLETS
from lib.openfood_env import WALLET_ALL_OUR_BATCH_LOT
from lib.openfood_env import WALLET_ALL_OUR_PO
from lib.openfood_env import WALLET_ALL_CUSTOMER_PO
from lib.openfood_env import CUSTOMER_RADDRESS

from dotenv import load_dotenv
from lib import transaction, bitcoin
from lib import rpclib
from lib.transaction import Transaction
from slickrpc import Proxy
import subprocess
import requests
import json
load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00012111
SATS_10K = 0.00010000

RPC = ""
KV1RPC = ""
URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
URL_openfood_API_ORGANIZATION = openfood_API_BASE_URL + openfood_API_ORGANIZATION
URL_openfood_API_ORGANIZATION_BATCH = openfood_API_BASE_URL + openfood_API_ORGANIZATION_BATCH


# helper methods
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def connect_node():
    global RPC
    print("Connecting to: " + KOMODO_NODE + ":" + RPC_PORT)
    RPC = Proxy("http://" + RPC_USER + ":" + RPC_PASSWORD + "@" + KOMODO_NODE + ":" + RPC_PORT)
    return True


def connect_kv1_node():
    global KV1RPC
    print("Connecting KV to: " + KV1_NODE + ":" + KV1_RPC_PORT)
    KV1RPC = Proxy("http://" + KV1_RPC_USER + ":" + KV1_RPC_PASSWORD + "@" + KV1_NODE + ":" + KV1_RPC_PORT)
    return True


def kvupdate_wrapper(kv_key, kv_value, kv_days, kv_passphrase):
    txid = rpclib.kvupdate(KV1RPC, kv_key, kv_value, kv_days, kv_passphrase)
    return txid


def kvsearch_wrapper(kv_key):
    kv_response = rpclib.kvsearch(KV1RPC, kv_key)
    return kv_response


# test skipped
def oracle_create(name, description, data_type):
    or_responce = rpclib.oracles_create(RPC, name, description, data_type)
    return or_responce


# test skipped
def oracle_fund(or_id):
    or_responce = rpclib.oracles_fund(RPC, or_id)
    return or_responce


# test skipped
def oracle_register(or_id, data_fee):
    or_responce = rpclib.oracles_register(RPC, or_id, data_fee)
    return or_responce


# test skipped
def oracle_subscribe(or_id, publisher_id, data_fee):
    or_responce = rpclib.oracles_subscribe(RPC, or_id, publisher_id, data_fee)
    return or_responce


# test skipped
def oracle_info(or_id):
    or_responce = rpclib.oracles_info(RPC, or_id)
    return or_responce


# test skipped
def oracle_data(or_id, hex_string):
    or_responce = rpclib.oracles_data(RPC, or_id, hex_string)
    return or_responce


# test skipped
def oracle_list():
    or_responce = rpclib.oracles_list(RPC)
    return or_responce


# test skipped
def oracle_samples(oracletxid, batonutxo, num):
    or_responce = rpclib.oracles_samples(RPC, oracletxid, batonutxo, num)
    return or_responce


def find_oracleid_with_pubkey(pubkey):
	or_responce = oracle_list()
	for oracle in or_responce:
		oracle = oracle_info(oracle)
		for registered in oracle['registered']:
			if registered['publisher'] == pubkey:
				return oracle['txid']


def sendtoaddress_wrapper(to_address, amount):
    send_amount = round(amount, 10)
    txid = rpclib.sendtoaddress(RPC, to_address, send_amount)
    return txid


def sendmany_wrapper(from_address, recipients_json):
    txid = rpclib.sendmany(RPC, from_address, recipients_json)
    return txid


def signmessage_wrapper(data):
    signed_data = rpclib.signmessage(RPC, THIS_NODE_RADDRESS, data)
    return signed_data


def housekeeping_tx():
    return sendtoaddress_wrapper(HOUSEKEEPING_RADDRESS, SCRIPT_VERSION)


def sendtoaddressWrapper(address, amount, amount_multiplier):
    print("Deprecated: use sendtoaddress_wrapper")
    send_amount = round(amount * amount_multiplier, 10)  # rounding 10??
    txid = rpclib.sendtoaddress(RPC, address, send_amount)
    return txid


def check_sync():
    general_info = rpclib.getinfo(RPC)
    sync = general_info['longestchain'] - general_info['blocks']

    print("Chain info.  Longest chain, blocks, sync diff")
    print(general_info['longestchain'])

    print(general_info['blocks'])

    print(sync)

    if sync >= BLOCKNOTIFY_CHAINSYNC_LIMIT:
        print('the chain is not synced, try again later')
        exit()

    print("Chain is synced")
    return sync


# test skipped
def get_this_node_raddress():
    return THIS_NODE_RADDRESS


def check_node_wallet():
    # check wallet management
    try:
        print("Validating node wallet with " + THIS_NODE_RADDRESS)
        is_mine = rpclib.validateaddress(RPC, THIS_NODE_RADDRESS)['ismine']
        print(is_mine)
        if is_mine is False:
            rpclib.importprivkey(RPC, THIS_NODE_WIF)
        is_mine = rpclib.validateaddress(RPC, THIS_NODE_RADDRESS)['ismine']
        return is_mine
    except Exception as e:
        print(e)
        print("## CHECK NODE WALLET ERROR ##")
        print("# Things that could be wrong:")
        print("# Wallet is not imported on this node or wallet mismatch to env")
        print("# Node is not available. Check debug.log for details")
        print("# If node is rescanning, will take a short while")
        print("# If changing wallet & env, rescan will occur")
        print("# Exiting.")
        print("##")
        exit()


def check_kv1_wallet():
    # check wallet management
    try:
        print("Validating kv1 wallet with " + THIS_NODE_RADDRESS)
        is_mine = rpclib.validateaddress(KV1RPC, THIS_NODE_RADDRESS)['ismine']
        print(is_mine)
        if is_mine is False:
            rpclib.importprivkey(KV1RPC, THIS_NODE_WIF)
        is_mine = rpclib.validateaddress(KV1RPC, THIS_NODE_RADDRESS)['ismine']
        return is_mine
    except Exception as e:
        print(e)
        print("## CHECK KV1 WALLET ERROR ##")
        print("# Things that could be wrong:")
        print("# Wallet is not imported on this node or wallet mismatch to env")
        print("# Node is not available. Check debug.log for details")
        print("# If node is rescanning, will take a short while")
        print("# If changing wallet & env, rescan will occur")
        print("# Exiting.")
        print("##")
        exit()


# test skipped
def generate_pool_wallets():
    wallet_all_our_po = getOfflineWalletByName(WALLET_ALL_OUR_PO)
    wallet_all_our_batch = getOfflineWalletByName(WALLET_ALL_OUR_BATCH_LOT)
    wallet_all_customer_po = getOfflineWalletByName(WALLET_ALL_CUSTOMER_PO)
    pool_wallets = {}
    pool_wallets[str(WALLET_ALL_OUR_PO)] = wallet_all_our_po["address"]
    pool_wallets[str(WALLET_ALL_OUR_BATCH_LOT)] = wallet_all_our_batch["address"]
    pool_wallets[str(WALLET_ALL_CUSTOMER_PO)] = wallet_all_customer_po["address"]
    print("pool wallets: " + json.dumps(pool_wallets))
    return pool_wallets


# test skipped
def verify_kv_pool_wallets():
    pool_wallets = generate_pool_wallets()
    print("Verifying pool wallets in KV1")
    org_kv1_key_pool_wallets = THIS_NODE_RADDRESS + KV1_ORG_POOL_WALLETS
    kv_response = kvsearch_wrapper(org_kv1_key_pool_wallets)
    if( kv_response.get("error")):
        print("Updating with a value")
        kv_response = kvupdate_wrapper(org_kv1_key_pool_wallets, json.dumps(pool_wallets), "3", "password")
        print(kv_response)
    else:
        print("kv exists for pool wallets")


# test skipped
def organization_get_pool_wallets_by_raddress(raddress):
    print("GET POOL WALLETS BY RADDRESS: " + raddress)
    kv_response = kvsearch_wrapper(raddress + KV1_ORG_POOL_WALLETS)
    return kv_response


# test skipped
def kv_save_batch_to_raddress(batch, raddress):
    kv_response = kvupdate_wrapper(batch, raddress, "100", "password")
    return kv_response


# test skipped
def kv_save_raddress_to_data(raddress, data):
    kv_response = kvupdate_wrapper(raddress, data, "100", "password")
    return kv_response


# test skipped
def kv_get_by_raddress(raddress):
    kv_response = kvsearch_wrapper(raddress)
    return kv_response


# deprecated
def fund_offline_wallet(offline_wallet_raddress):
    print("DEPRECATED WARNING: fund_offline_wallet")
    json_object = {
     offline_wallet_raddress: 11.2109
     }
    sendmany_txid = sendmany_wrapper(THIS_NODE_RADDRESS, json_object)
    return sendmany_txid


def fund_offline_wallet2(offline_wallet_raddress, send_amount):
    json_object = {
     offline_wallet_raddress: send_amount
     }
    sendmany_txid = sendmany_wrapper(THIS_NODE_RADDRESS, json_object)
    return sendmany_txid


def is_below_threshold_balance(check_this, balance_threshold):
    if( check_this < balance_threshold * 100000000 ):
        return True

def check_offline_wallets():
    print("Check offline wallets: getXXXWallet, getBalance (if low then fund), getUTXOCount")
    wallet_delivery_date = getOfflineWalletByName(WALLET_DELIVERY_DATE)
    wallet_pon = getOfflineWalletByName(WALLET_PON)
    wallet_tin = getOfflineWalletByName(WALLET_TIN)
    wallet_prod_date = getOfflineWalletByName(WALLET_PROD_DATE)
    wallet_julian_start = getOfflineWalletByName(WALLET_JULIAN_START)
    wallet_julian_stop = getOfflineWalletByName(WALLET_JULIAN_STOP)
    wallet_origin_country = getOfflineWalletByName(WALLET_ORIGIN_COUNTRY)
    wallet_bb_date = getOfflineWalletByName(WALLET_BB_DATE)
    wallet_mass_balance = getOfflineWalletByName(WALLET_MASS_BALANCE)

    # print("Checking delivery date wallet: " + wallet_delivery_date['address'])
    # check balance
    wallet_delivery_date_balance = int(explorer_get_balance(wallet_delivery_date['address']))
    print(wallet_delivery_date_balance)
    if is_below_threshold_balance(wallet_delivery_date_balance, WALLET_DELIVERY_DATE_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_DELIVERY_DATE + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_delivery_date['address'], WALLET_DELIVERY_DATE_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_mass_balance_balance = int(explorer_get_balance(wallet_mass_balance['address']))
    print(wallet_mass_balance)
    if is_below_threshold_balance(wallet_mass_balance_balance, WALLET_MASS_BALANCE_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_MASS_BALANCE + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_mass_balance['address'], WALLET_MASS_BALANCE_THRESHOLD_UTXO_VALUE)
        print(funding_txid)

    wallet_pon_balance = int(explorer_get_balance(wallet_pon['address']))
    print(wallet_pon_balance)
    if is_below_threshold_balance(wallet_pon_balance, WALLET_PON_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_PON + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_pon['address'], WALLET_PON_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_tin_balance = int(explorer_get_balance(wallet_tin['address']))
    print(wallet_tin_balance)
    if is_below_threshold_balance(wallet_tin_balance, WALLET_TIN_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_TIN + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_tin['address'], WALLET_TIN_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_prod_date_balance = int(explorer_get_balance(wallet_prod_date['address']))
    print(wallet_prod_date_balance)
    if is_below_threshold_balance(wallet_prod_date_balance, WALLET_PROD_DATE_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_PROD_DATE + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_prod_date['address'], WALLET_PROD_DATE_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_julian_start_balance = int(explorer_get_balance(wallet_julian_start['address']))
    print(wallet_julian_start_balance)
    if is_below_threshold_balance(wallet_julian_start_balance, WALLET_JULIAN_START_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_JULIAN_START + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_julian_start['address'], WALLET_JULIAN_START_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_julian_stop_balance = int(explorer_get_balance(wallet_julian_stop['address']))
    print(wallet_julian_stop_balance)
    if is_below_threshold_balance(wallet_julian_stop_balance, WALLET_JULIAN_STOP_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_JULIAN_STOP + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_julian_stop['address'], WALLET_JULIAN_STOP_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_origin_country_balance = int(explorer_get_balance(wallet_origin_country['address']))
    print(wallet_origin_country_balance)
    if is_below_threshold_balance(wallet_origin_country_balance, WALLET_ORIGIN_COUNTRY_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_ORIGIN_COUNTRY + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_origin_country['address'], WALLET_ORIGIN_COUNTRY_THRESHOLD_BALANCE)
        print(funding_txid)

    wallet_bb_date_balance = int(explorer_get_balance(wallet_bb_date['address']))
    print(wallet_bb_date_balance)
    if is_below_threshold_balance(wallet_bb_date_balance, WALLET_BB_DATE_THRESHOLD_BALANCE):
        print("FUND the " + WALLET_BB_DATE + " wallet because balance low")
        funding_txid = fund_offline_wallet2(wallet_bb_date['address'], WALLET_BB_DATE_THRESHOLD_BALANCE)
        print(funding_txid)


    # check utxo count
    utxo_count = explorer_get_utxos(wallet_delivery_date['address'])
    print(utxo_count)
    return utxo_count
    # next needs to be manual tx, sendmany does not function like this
    # if low, fund with sendmany by adding threshold balance x3 utxo threshold
    # if( len(utxo_count) < WALLET_DELIVERY_DATE_THRESHOLD_UTXO):
        # print("FUND the wallet because low utxo count")
        # fund_offline_wallet(wallet_delivery_date['address'])


# test skipped
def organization_certificate_noraddress(url, org_id, THIS_NODE_RADDRESS):
    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(e)

    certs_no_addy = res.text
    certs_no_addy = json.loads(certs_no_addy)
    # the issuer, issue date, expiry date, identifier (not the db id, the certificate serial number / identfier)

    for cert in certs_no_addy:
        raw_json = {
            "issuer": cert['issuer'],
            "issue_date": cert['date_issue'],
            "expiry_date": cert['date_expiry'],
            "identfier": cert['identifier']
        }
        raw_json = json.dumps(raw_json)
        addy = gen_wallet(raw_json)
        # id = str(cert['id'])
        # url = IMPORT_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + id + "/"

        try:
            data = {"raddress": addy['address'], "pubkey": addy['pubkey']}
            res = requests.patch(url, data=data)
        except Exception as e:
            raise Exception(e)


def explorer_get_utxos(querywallet):
    print("Get UTXO for wallet " + querywallet)
    # INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/{querywallet}/utxo"
    INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/" + querywallet + "/utxo"
    try:
        res = requests.get(EXPLORER_URL + INSIGHT_API_KOMODO_ADDRESS_UTXO)
    except Exception as e:
        raise Exception(e)
    # vouts = json.loads(res.text)
    # for vout in vouts:
        # print(vout['txid'] + " " + str(vout['vout']) + " " + str(vout['amount']) + " " + str(vout['satoshis']))
    return res.text


def explorer_get_balance(querywallet):
    print("Get balance for wallet: " + querywallet)
    INSIGHT_API_KOMODO_ADDRESS_BALANCE = "insight-api-komodo/addr/" + querywallet + "/balance"
    try:
        res = requests.get(EXPLORER_URL + INSIGHT_API_KOMODO_ADDRESS_BALANCE)
    except Exception as e:
        raise Exception(e)
    return res.text


def createrawtx_wrapper(txids, vouts, to_address, amount):
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


def createrawtxwithchange(txids, vouts, to_address, amount, change_address, change_amount):
    print(to_address)
    print(amount)
    print(change_address)
    print(change_amount)
    return rpclib.createrawtransactionwithchange(RPC, txids, vouts, to_address, amount, change_address, change_amount)


def createrawtx_split_wallet(txids, vouts, to_address, amount, change_address, change_amount):
    print(to_address)
    print(amount)
    print(change_address)
    print(change_amount)
    return rpclib.createrawtransactionsplit(RPC, txids, vouts, to_address, amount, change_address, change_amount)


def createrawtx(txids, vouts, to_address, amount):
    print("Deprecated: use createrawtx_wrapper")
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


# test skipped
def createrawtx7(utxos_json, num_utxo, to_address, to_amount, fee, change_address, split=False):
    # check createrawtx6 comments
    print("createrawtx7()")

    if( num_utxo == 0 ):
        print("ERROR: createrawtx_error, num_utxo == 0")
        return

    print("to address: " + str(to_address) + " , to amount: " + str(to_amount))
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for utxo in utxos:
        if (utxo['amount'] > 0.2 and utxo['confirmations'] > 2) and count < num_utxo:
            count = count + 1
            vout_as_array = [utxo['vout']]
            txid_as_array = [utxo['txid']]
            txids.extend(txid_as_array)
            vouts.extend(vout_as_array)
            amount = amount + utxo['amount']
            amounts.extend([utxo['satoshis']])

    if( amount > to_amount ):
        change_amount = round(amount - fee - to_amount, 10)
    else:
        # TODO
        print("### ERROR ### Needs to be caught, the to_amount is larger than the utxo amount, need more utxos")
        return
        # change_amount = round(to_amount - amount - fee, 10)
    print("amount >=")
    print(amount)
    print("to_amount + change_amount + fee")
    print(to_amount)
    print(float(change_amount))
    print(fee)
    rawtx = ""
    if( change_amount < 0.01 ):
        print("Change too low, sending as miner fee " + str(change_amount))
        change_amount = 0
        rawtx = createrawtx(txids, vouts, to_address, round(amount - fee, 10))

    else:
        if(split):
            print("Creating raw tx for split_wallet")
            rawtx = createrawtx_split_wallet(txids, vouts, to_address, to_amount, change_address, float(change_amount))
        else:
            print("Creating raw tx with change")
            rawtx = createrawtxwithchange(txids, vouts, to_address, to_amount, change_address, float(change_amount))

    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    print("raw tx created: ")
    print(rawtx_info)

    return rawtx_info

def createrawtx_dev(utxos_json, to_address, to_amount, fee, change_address):
    # check if utxos_json list is not empty
    num_utxo = len(utxos_json)
    if( num_utxo == 0 ):
        print("utxos are required (list)")
        return

    # The limitations of the current createrawtx code are:
    # 1. if value needing to send is more than the selected utxo value, then we cannot send.
    # 2. if failure to send, no retry currently.

    # calculate utxos amount
    amount = utxo_bundle_amount(utxos_json)

    # amount after fee
    change_amount = round(amount - fee, 10)

    # stop if utxos amount (after fee) < to_amount
    if change_amount < to_amount:
        print(
            'insufficient amount',
            f'total amount: {amount}',
            f'send amount: {to_amount}',
            f'fee: {fee}'
        )
        return

    # get all txid utxos and convert to list
    txids = [d['txid'] for d in utxos_json]

    # get all vout utxos and convert to list
    vouts = [d['vout'] for d in utxos_json]

    # satoshis
    satoshis = [d['satoshis'] for d in utxos_json]

    # change amount (reduced by to_amount)
    change_amount = round(change_amount - to_amount, 10)

    # rawtx = createrawtxwithchange(txids, vouts, to_address, to_amount, change_address, change_amount)
    rawtx = createrawtxwithchange(txids, vouts, to_address, to_amount, change_address, float(change_amount))

    # return rawtx and satoshis (append to list)
    return [{"rawtx": rawtx}, {"satoshis": satoshis}]

# test skipped
def createrawtx6(utxos_json, num_utxo, to_address, to_amount, fee, change_address):
    print(to_address)
    # check this file in commit https://github.com/The-New-Fork/blocknotify-python/commit/f91a148b18840aaf08d7c7736045a8c924bd236b
    # for to_amount.  When a wallet had no utxos, the resulting change was -0.00123, some sort of mis-naming maybe?
    #to_amount = 0.00123
    # MITIGATE ^^
    if( num_utxo == 0 ):
        return

    print(to_amount)
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    # utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        if (objects['amount'] > 0.2 and objects['confirmations'] > 2) and count < num_utxo:
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    # check this file in commit https://github.com/The-New-Fork/blocknotify-python/commit/f91a148b18840aaf08d7c7736045a8c924bd236b
    # for to_amount.  When a wallet had no utxos, the resulting change was -0.00123, some sort of mis-naming maybe?
    #to_amount = 0.00123
    # change_tmp = 0
    if( amount > to_amount ):
        change_amount = round(amount - fee - to_amount, 10)
    else:
        # TODO
        print("### ERROR ### Needs to be caught, the to_amount is larger than the utxo amount, need more utxos")
        change_amount = round(to_amount - amount - fee, 10)
    print("AMOUNTS: amount, #to_amount, change_amount, fee")
    print(amount)
    print(to_amount)
    print(float(change_amount))
    print(fee)
    rawtx = ""
    if( change_amount < 0.01 ):
        print("Change too low, sending as miner fee " + str(change_amount))
        change_amount = 0
        rawtx = createrawtx(txids, vouts, to_address, round(amount - fee, 10))

    else:
        rawtx = createrawtxwithchange(txids, vouts, to_address, to_amount, change_address, float(change_amount))

    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info

# deprecated
def createrawtx5(utxos_json, num_utxo, to_address, fee, change_address):
    print("DEPRECATED WARNING: createrawtx5")
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    # utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        if (objects['amount'] > 0.00005 and objects['confirmations'] > 2) and count < num_utxo:
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    # check this file in commit https://github.com/The-New-Fork/blocknotify-python/commit/f91a148b18840aaf08d7c7736045a8c924bd236b
    # for to_amount.  When a wallet had no utxos, the resulting change was -0.00123, some sort of mis-naming maybe?
    #to_amount = 0.00123
    change_tmp = 0
    change_amount = round(amount - fee - change_tmp, 10)
    print("AMOUNTS: amount, #to_amount, change_amount, fee")
    print(amount)
    # print(to_amount)
    print(change_amount)
    print(fee)

    # rawtx = createrawtxwithchange(txids, vouts, to_address, to_amount, change_address, change_amount)
    rawtx = createrawtxwithchange(txids, vouts, to_address, change_tmp, change_address, change_amount)
    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info

# deprecated
def createrawtx4(utxos_json, num_utxo, to_address, fee):
    print("DEPRECATED WARNING: createrawtx4")
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        if (objects['amount'] > 0.00005) and count < num_utxo:
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    amount = round(amount, 10)
    print("AMOUNT")
    print(amount)

    rawtx = createrawtx(txids, vouts, to_address, round(amount - fee, 10))
    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info


def decoderawtx_wrapper(tx):
    return rpclib.decoderawtransaction(RPC, tx)


def decoderawtx(tx):
    print("Deprecated: use decoderawtx_wrapper(tx)")
    return rpclib.decoderawtransaction(RPC, tx)


def signtx(kmd_unsigned_tx_serialized, amounts, wif):
    txin_type, privkey, compressed = bitcoin.deserialize_privkey(wif)
    pubkey = bitcoin.public_key_from_private_key(privkey, compressed)

    jsontx = transaction.deserialize(kmd_unsigned_tx_serialized)
    inputs = jsontx.get('inputs')
    outputs = jsontx.get('outputs')
    locktime = jsontx.get('lockTime', 0)
    outputs_formatted = []
    # print("\n###### IN SIGNTX FUNCTION #####\n")
    # print(jsontx)
    # print(inputs)
    # print(outputs)
    # print(locktime)

    for txout in outputs:
        outputs_formatted.append([txout['type'], txout['address'], (txout['value'])])
        print("Value of out before miner fee: " + str(txout['value']))
        print("Value of out: " + str(txout['value']))

    # print("\nOutputs formatted:\n")
    # print(outputs_formatted)

    for txin in inputs:
        txin['type'] = txin_type
        txin['x_pubkeys'] = [pubkey]
        txin['pubkeys'] = [pubkey]
        txin['signatures'] = [None]
        txin['num_sig'] = 1
        txin['address'] = bitcoin.address_from_private_key(wif)
        txin['value'] = amounts[inputs.index(txin)]  # required for preimage calc

    tx = Transaction.from_io(inputs, outputs_formatted, locktime=locktime)
    # print("### TX before signing###")
    # print(tx)
    # print("### END TX ###")
    tx.sign({pubkey: (privkey, compressed)})

    # print("\nSigned tx:\n")
    # print(tx.serialize())
    # print("Return from signtx")
    return tx.serialize()


# test skipped
def broadcast_via_explorer(explorer_url, signedtx):
    INSIGHT_API_BROADCAST_TX = "insight-api-komodo/tx/send"
    params = {'rawtx': signedtx}
    url = explorer_url + INSIGHT_API_BROADCAST_TX
    print("Broadcast via " + url)

    try:
        broadcast_res = requests.post(url, data=params)
    except Exception as e:
        print(e)

    print(broadcast_res.text)
    broadcast_res = json.loads(broadcast_res.text)
    return broadcast_res['txid']


def gen_wallet(data, label='NoLabelOK'):
    print("Creating a %s address signing with %s and data %s" % (label, THIS_NODE_RADDRESS, data))
    signed_data = rpclib.signmessage(RPC, THIS_NODE_RADDRESS, data)
    # print("Signed data is %s" % (signed_data))
    new_wallet_json = subprocess.getoutput("php genwallet.php " + signed_data)
    print("Created wallet %s" % (new_wallet_json))

    new_wallet = json.loads(new_wallet_json)

    return new_wallet


def getOfflineWalletByName(name):
    obj = {
        "name": name
    }
    raw_json = json.dumps(obj)
    log_label = name
    offline_wallet = gen_wallet(raw_json, log_label)
    return offline_wallet


# test skipped
def dateToSatoshi(date):
    formatDate = int(date.replace('-', ''))
    return round(formatDate/100000000, 10)

  
def sendToBatchMassBalance(batch_raddress, mass_balance_value):
    # delivery date
    print("SEND MASS BALANCE")
    mass_balance_wallet = getOfflineWalletByName(WALLET_MASS_BALANCE)
    utxos_json = explorer_get_utxos(mass_balance_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx6(utxos_json, 1, batch_raddress, round(mass_balance_value/1, 10), 0, mass_balance_wallet['address'])
    print("MASS BALANCE RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], mass_balance_wallet['wif'])
    mass_balance_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = mass_balance_wallet['address']
    # txid = sendtoaddressWrapper(batch_raddress, date_as_satoshi/100000000, 1)
    return mass_balance_txid


# deprecated
def massBalanceIntoApi(mass_balance_txid, mass_balance_value, id):
   url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_BATCH + str(id) + "/"
  # data = { "mass_balance_value":mass_balance_value,
   #"mass_balance_txid":mass_balance_txid}
   data = {
    #"id": 1,
    #"identifier": "ID-8038356",
    #"jds": 96,
    #"jde": 964,
    #"date_production_start": "2020-06-09",
    #"date_best_before": "2020-06-09",
    #"delivery_date": None,
    #"origin_country": "DE",
    #"pubkey": "027e0232fe7c10751bf214206d2c03c4ae4d7ea5f1eeb5c3cd5136a19ddadd4cee",
    #"raddress": "RTSEYsRCMzkWIpUBCLXWGHqdtQgjDDilVN",
    "mass_balance_value": mass_balance_value,
    "mass_balance_txid": mass_balance_txid,
    #"organization": 1
   }
   answere = requests.patch(url, data=data)
   print("post: " + answere.text)
   return answere

  
def rToId(batch_raddress):
   url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_BATCH
   batches = getWrapper(url)
   batches = json.loads(batches)
   for batch in batches:
       if batch['raddress'] == batch_raddress:
            return batch['id']
 
   return None


# deprecated
# no test
def sendAndPatchMassBalance(batch_raddress, mass_balance_value):
   txid = sendToBatchMassBalance(batch_raddress, mass_balance_value)
   id = rToId(batch_raddress)
   answere = massBalanceIntoApi(txid, mass_balance_value, id)
   return answere


# no test
def split_wallet1():
    print("split_wallet1()")
    delivery_date_wallet = getOfflineWalletByName(WALLET_DELIVERY_DATE)
    utxos_json = explorer_get_utxos(delivery_date_wallet['address'])


# test skipped
def sendToBatchDeliveryDate(batch_raddress, delivery_date):
    # delivery date
    print("SEND DELIVERY DATE")
    date_as_satoshi = dateToSatoshi(delivery_date)
    print(date_as_satoshi)
    delivery_date_wallet = getOfflineWalletByName(WALLET_DELIVERY_DATE)
    utxos_json = explorer_get_utxos(delivery_date_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, date_as_satoshi, 0, delivery_date_wallet['address'])
    print("DELIVERY DATE RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], delivery_date_wallet['wif'])
    deliverydate_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    return deliverydate_txid


# test skipped
def sendToBatchPDS(batch_raddress, production_date):
    # delivery date
    print("SEND PRODUCTION DATE")
    date_as_satoshi = dateToSatoshi(production_date)
    print(date_as_satoshi)
    production_date_wallet = getOfflineWalletByName(WALLET_PROD_DATE)
    utxos_json = explorer_get_utxos(production_date_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, date_as_satoshi, 0, production_date_wallet['address'])
    print("PROD DATE RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], production_date_wallet['wif'])
    proddate_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    return proddate_txid


# test skipped
def sendToBatchBBD(batch_raddress, bb_date):
    # delivery date
    print("SEND BB DATE")
    date_as_satoshi = dateToSatoshi(bb_date)
    print(date_as_satoshi)
    bb_date_wallet = getOfflineWalletByName(WALLET_BB_DATE)
    utxos_json = explorer_get_utxos(bb_date_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, date_as_satoshi, 0, bb_date_wallet['address'])
    print("BB DATE RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], bb_date_wallet['wif'])
    bbdate_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    return bbdate_txid


# test skipped
def sendToBatchPON(batch_raddress, pon):
    # purchase order number
    print("SEND PON, check PON is accurate")
    pon_as_satoshi = dateToSatoshi(pon)
    print(pon_as_satoshi)
    pon_wallet = getOfflineWalletByName(WALLET_PON)
    utxos_json = explorer_get_utxos(pon_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, pon_as_satoshi, 0, pon_wallet['address'])
    print("PON RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], pon_wallet['wif'])
    pon_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = pon_wallet['address']
    return pon_txid


# test skipped
def sendToBatchTIN(batch_raddress, tin):
    # purchase order number
    print("SEND PON, check PON is accurate")
    tin_as_satoshi = dateToSatoshi(tin)
    print(tin_as_satoshi)
    tin_wallet = getOfflineWalletByName(WALLET_TIN)
    utxos_json = explorer_get_utxos(tin_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, tin_as_satoshi, 0, tin_wallet['address'])
    print("PON RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], tin_wallet['wif'])
    tin_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    return tin_txid


# test skipped
def sendToBatchPL(batch_raddress, pl):
    # product locationcreaterawtx7
    print("SEND PL, check PL is accurate")
    pl_wallet = getOfflineWalletByName(pl)
    utxos_json = explorer_get_utxos(pl_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, 0.0001, 0, pl_wallet['address'])
    print("PL RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], pl_wallet['wif'])
    pl_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = pl_wallet['address']
    return pl_txid


# test skipped
def sendToBatchJDS(batch_raddress, jds):
    # product locationcreaterawtx7
    jds_wallet = getOfflineWalletByName(WALLET_JULIAN_START)
    utxos_json = explorer_get_utxos(jds_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, 0.0001, 0, jds_wallet['address'])
    print("JDStart RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], jds_wallet['wif'])
    jds_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = jds_wallet['address']
    return jds_txid


# test skipped
def sendToBatchJDE(batch_raddress, jds):
    # product locationcreaterawtx7
    jds_wallet = getOfflineWalletByName(WALLET_JULIAN_STOP)
    utxos_json = explorer_get_utxos(jds_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, 0.0001, 0, jds_wallet['address'])
    print("JDStop RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], jds_wallet['wif'])
    jds_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = jds_wallet['address']
    return jds_txid


# test skipped
def sendToBatchPC(batch_raddress, pc):
    # product locationcreaterawtx7
    pc_wallet = getOfflineWalletByName(WALLET_ORIGIN_COUNTRY)
    utxos_json = explorer_get_utxos(pc_wallet['address'])
    print(utxos_json)
    # works sending 0
    # rawtx_info = createrawtx5(utxos_json, 1, batch_raddress, 0, delivery_date_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, batch_raddress, 0.0001, 0, pc_wallet['address'])
    print("Product Country RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], pc_wallet['wif'])
    pc_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = pc_wallet['address']
    return pc_txid


# no test
def split_wallet_PL(THIS_NODE_RADDRESS, pl):
    # product locationcreaterawtx7
    print("Split PL")
    pl_wallet = getOfflineWalletByName(pl)
    utxos_json = explorer_get_utxos(pl_wallet['address'])
    rawtx_info = createrawtx7(utxos_json, 1, THIS_NODE_RADDRESS, 0.1, 0, pl_wallet['address'], True)
    print("PL RAWTX: " + str(rawtx_info))
    signedtx = signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], pl_wallet['wif'])
    pl_txid = broadcast_via_explorer(EXPLORER_URL, signedtx)
    raddress = pl_wallet['address']
    return pl_txid


# test skipped, can be templated for re-use
def offlineWalletGenerator_fromObjectData_certificate(objectData):
    obj = {
        "issuer": objectData['issuer'],
        "issue_date": objectData['date_issue'],
        "expiry_date": objectData['date_expiry'],
        "identfier": objectData['identifier']
    }

    print(obj)
    log_label = objectData['identifier']
    raw_json = json.dumps(obj)
    
    print("libopenfood->offlineWalletGenerator object data as json: " + raw_json)

    offline_wallet = gen_wallet(raw_json, log_label)

    return offline_wallet


def utxo_bundle_amount(utxos_obj):
    count = 0
    list_of_ids = []
    list_of_vouts = []
    amount = 0

    for objects in utxos_obj:
        if (objects['amount']):
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            list_of_ids.extend(easy_typeing)
            list_of_vouts.extend(easy_typeing2)
            amount = amount + objects['amount']

    amount = round(amount, 10)
    return amount


def get_batches_no_timestamp():
    print("***** start import api timestamping integrity - raw/refresco/require_integrity/")
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
    print("Trying: " + url)

    try:
        res = requests.get(url)
    except Exception as e:
        print("###### REQUIRE INTEGRITY URL ERROR: ", e)
        print("20201020 - url not sending nice response " + url)

    print(res.text)

    raw_json = res.text
    batches_no_timestamp = ""

    try:
        batches_no_timestamp = json.loads(raw_json)
    except Exception as e:
        print("10009 failed to parse to json because of", e)

    print("***** New batch requires timestamping: " + str(len(batches_no_timestamp)))
    return batches_no_timestamp


def get_batches():
    print("10009 start import api - raw/refresco")
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_PATH
    print("Trying: " + url)

    try:
        res = requests.get(url)
    except Exception as e:
        print("###### REQUIRE INTEGRITY URL ERROR: ", e)
        print("20201020 - url not sending nice response " + url)

    print(res.text)

    raw_json = res.text
    batches = ""

    try:
        batches = json.loads(raw_json)
    except Exception as e:
        print("10009 failed to parse to json because of", e)

    print("New batch requires timestamping: " + str(len(batches)))
    return batches


def get_certificates_no_timestamp():
    url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS
    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(e)

    certs_no_addy = json.loads(res.text)
    return certs_no_addy


# test skipped
def fund_certificate(certificate_address):
    txid = sendtoaddress_wrapper(certificate_address, FUNDING_AMOUNT_CERTIFICATE)
    return txid


def postWrapper(url, data):
    res = requests.post(url, data=data)
    if(res.status_code == 200 | res.status_code == 201):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


def putWrapper(url, data):
    res = requests.put(url, data=data)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


def patchWrapper(url, data):
    res = requests.patch(url, data=data)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


def getWrapper(url):
    res = requests.get(url)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


def get_jcapi_organization():
    print("GET openfood-api organization query: " + URL_openfood_API_ORGANIZATION + "?raddress=" + THIS_NODE_RADDRESS)
    res = getWrapper(URL_openfood_API_ORGANIZATION + "?raddress=" + THIS_NODE_RADDRESS)
    print(res)
    organizations = json.loads(res)
    # TODO E721 do not compare types, use "isinstance()" pep8
    if type(organizations) == type(['d', 'f']):
        return organizations[0]
    return organizations


# test skipped
def batch_wallets_generate_timestamping(batchObj, import_id):
    json_batch = json.dumps(batchObj)
    # anfp_wallet = gen_wallet(json_batch['anfp'], "anfp")
    # pon_wallet = gen_wallet(json_batch['pon'], "pon")
    bnfp_wallet = gen_wallet(batchObj['bnfp'], "bnfp")
    # pds_wallet = openfood.gen_wallet(data['pds'], "pds")
    # jds_wallet = openfood.gen_wallet(data['jds'], "jds")
    # jde_wallet = openfood.gen_wallet(data['jde'], "jde")
    # bbd_wallet = openfood.gen_wallet(data['bbd'], "bbd")
    # pc_wallet = openfood.gen_wallet(data['pc'], "pc")
    integrity_address = gen_wallet(json_batch, "integrity address")
    print("Timestamp-integrity raddress: " + integrity_address['address'])
    data = {'name': 'timestamping',
            'integrity_address': integrity_address['address'],
            'batch': import_id,
            'batch_lot_raddress': bnfp_wallet['address']
            }

    batch_wallets_update_response = postWrapper(URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH, data)
    print("POST response: " + batch_wallets_update_response)
    return json.loads(batch_wallets_update_response)


def batch_wallets_timestamping_update(batch_integrity):
    batch_integrity_url = URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + batch_integrity['id'] + "/"
    print(batch_integrity)
    batch_integrity_response = putWrapper(batch_integrity_url, batch_integrity)
    return batch_integrity_response


def batch_wallets_timestamping_start(batch_integrity, start_txid):
    batch_integrity_url = URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + batch_integrity['id'] + "/"
    print(batch_integrity)
    batch_integrity['integrity_pre_tx'] = start_txid
    print(batch_integrity)
    # data = {'name': 'chris', 'integrity_address': integrity_address[
    #    'address'], 'integrity_pre_tx': integrity_start_txid, 'batch_lot_raddress': bnfp_wallet['address']}

    batch_integrity_start_response = putWrapper(batch_integrity_url, batch_integrity)
    return batch_integrity_start_response


def batch_wallets_timestamping_end(batch_integrity, end_txid):
    batch_integrity['integrity_post_tx'] = end_txid
    print(batch_integrity)
    batch_integrity_end_response = batch_wallets_timestamping_update(batch_integrity)
    return batch_integrity_end_response


def batch_wallets_fund_integrity_start(integrity_address):
    return sendtoaddress_wrapper(integrity_address, FUNDING_AMOUNT_TIMESTAMPING_START)


def batch_wallets_fund_integrity_end(integrity_address):
    return sendtoaddress_wrapper(integrity_address, FUNDING_AMOUNT_TIMESTAMPING_END)


# test skipped
def organization_get_our_pool_batch_wallet():
    kv_response = organization_get_pool_wallets_by_raddress(THIS_NODE_RADDRESS)
    print(kv_response)
    tmp = json.loads(kv_response['value'])
    tmp2 = str(tmp[WALLET_ALL_OUR_BATCH_LOT])
    return tmp2


# test skipped
def organization_get_our_pool_po_wallet():
    kv_response = organization_get_pool_wallets_by_raddress(THIS_NODE_RADDRESS)
    print(kv_response)
    tmp = json.loads(kv_response['value'])
    tmp2 = str(tmp[WALLET_ALL_OUR_PO])
    return tmp2


# test skipped
def organization_get_customer_po_wallet(CUSTOMER_RADDRESS):
    kv_response = organization_get_pool_wallets_by_raddress(CUSTOMER_RADDRESS)
    print(kv_response)
    tmp = json.loads(kv_response['value'])
    tmp2 = str(tmp[WALLET_ALL_OUR_PO])
    return tmp2


# test skipped
def organization_get_customer_batch_wallet(CUSTOMER_RADDRESS):
    kv_response = organization_get_pool_wallets_by_raddress(CUSTOMER_RADDRESS)
    print(kv_response)
    tmp = json.loads(kv_response['value'])
    tmp2 = str(tmp[WALLET_ALL_OUR_BATCH_LOT])
    return tmp2


def organization_send_batch_links(batch_integrity):
    sample_pool_po = "RWSVFtCJfRH5ErsXJCaz9YNVKx7PijxpoV"
    sample_pool_batch_lot = "R9X5CBJjmVmJe4a533hemBf6vCW2m3BAqH"
    pool_batch_wallet = organization_get_our_pool_batch_wallet()
    pool_po = organization_get_our_pool_po_wallet()
    print("MAIN WALLET " + THIS_NODE_RADDRESS + " SENDMANY TO BATCH_LOT (bnfp), POOL_PO (pon), POOL_BATCH_LOT")
    print(pool_batch_wallet)
    customer_pool_wallet = organization_get_customer_po_wallet(CUSTOMER_RADDRESS)
    print("CUSTOMER POOL WALLET: " + customer_pool_wallet)

    json_object = {

                    pool_batch_wallet: SCRIPT_VERSION,
                    pool_po: SCRIPT_VERSION,
                   batch_integrity['batch_lot_raddress']: SCRIPT_VERSION,
                   customer_pool_wallet: SCRIPT_VERSION
                   }
    sendmany_txid = sendmany_wrapper(THIS_NODE_RADDRESS, json_object)
    return sendmany_txid


# test skipped
def organization_send_batch_links2(batch_integrity, pon):
    pon_as_satoshi = dateToSatoshi(pon)
    pool_batch_wallet = organization_get_our_pool_batch_wallet()
    pool_po = organization_get_our_pool_po_wallet()
    customer_pool_wallet = organization_get_customer_po_wallet(CUSTOMER_RADDRESS)

    print("****** MAIN WALLET batch links sendmany ******* " + THIS_NODE_RADDRESS)
    print(pool_batch_wallet)
    print("CUSTOMER POOL WALLET: " + customer_pool_wallet)
    print("pon & pon as satoshi: " + pon + ":" + str(pon_as_satoshi))

    json_object = {

                    pool_batch_wallet: SCRIPT_VERSION,
                    pool_po: pon_as_satoshi,
                   batch_integrity['batch_lot_raddress']: SCRIPT_VERSION,
                   customer_pool_wallet: pon_as_satoshi
                   }
    sendmany_txid = sendmany_wrapper(THIS_NODE_RADDRESS, json_object)
    return sendmany_txid


# test skipped
def organization_send_batch_links3(batch_integrity, pon, bnfp):
    pon_as_satoshi = dateToSatoshi(pon)
    bnfp_as_satoshi = dateToSatoshi(bnfp)
    pool_batch_wallet = organization_get_our_pool_batch_wallet()
    pool_po = organization_get_our_pool_po_wallet()
    customer_pool_wallet = organization_get_customer_po_wallet(CUSTOMER_RADDRESS)

    print("****** MAIN WALLET batch links sendmany ******* " + THIS_NODE_RADDRESS)
    print(pool_batch_wallet)
    print("CUSTOMER POOL WALLET: " + customer_pool_wallet)
    print("pon & pon as satoshi: " + pon + ":" + str(pon_as_satoshi))

    json_object = {
                    pool_batch_wallet: bnfp_as_satoshi,
                    pool_po: pon_as_satoshi,
                    batch_integrity['batch_lot_raddress']: SATS_10K,
                    customer_pool_wallet: pon_as_satoshi
                   }
    sendmany_txid = sendmany_wrapper(THIS_NODE_RADDRESS, json_object)
    return sendmany_txid


def timestamping_save_batch_links(id, sendmany_txid):
    print("** txid ** (Main org wallet sendmany BATCH_LOT/POOL_PO/GTIN): " + sendmany_txid)
    tstx_data = {'sender_raddress': THIS_NODE_RADDRESS,
                 'tsintegrity': id, 'sender_name': 'ORG WALLET', 'txid': sendmany_txid}
    ts_response = postWrapper(URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH, tstx_data)
    print("POST ts_response: " + ts_response)
    return ts_response


# test skipped
def timestamping_save_certificate(id, sender_name, sender_wallet, certificate_txid):
    print("** txid ** (Certificate to batch_lot): " + certificate_txid)
    tstx_data = {'sender_raddress': sender_wallet['address'],
                 'tsintegrity': id, 'sender_name': sender_name, 'txid': certificate_txid}
    print(tstx_data)
    ts_response = postWrapper(URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH, tstx_data)
    print("POST ts_response: " + ts_response)
    return ts_response


# no test
def get_certificate_for_test(url):
    return getWrapper(url)


def get_certificate_for_batch():
    # TODO this is hardcoded, which is bad - needs to fetch by cert rules
    test_url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + "2/"
    certificate = json.loads(get_certificate_for_test(test_url))
    return certificate


# test skipped
def push_batch_data_consumer(jcapi_org_id, batch, batch_wallet):
        data = {'identifier': batch['bnfp'],
                'jds': batch['jds'],
                'jde': batch['jde'],
                'date_production_start': batch['pds'],
                'date_best_before': batch['bbd'],
                'origin_country': batch['pc'],
                'mass_balance': batch['mass'],
                'raddress': batch_wallet['address'],
                'pubkey': batch_wallet['pubkey'],
                'organization': jcapi_org_id}
        jcapi_response = postWrapper(URL_openfood_API_ORGANIZATION_BATCH, data=data)
        jcapi_batch_id = json.loads(jcapi_response)['id']
        print("BATCH ID @ openfood-API: " + str(jcapi_batch_id))
        return jcapi_response
