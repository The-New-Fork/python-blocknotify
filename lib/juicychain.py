# from lib.juicychain_env import MULTI_1X
# from lib.juicychain_env import MULTI_2X
# from lib.juicychain_env import MULTI_3X
# from lib.juicychain_env import MULTI_4X
# from lib.juicychain_env import MULTI_5X
from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import THIS_NODE_WIF
from lib.juicychain_env import BLOCKNOTIFY_CHAINSYNC_LIMIT
from lib.juicychain_env import HOUSEKEEPING_ADDRESS
from lib.juicychain_env import IMPORT_API_BASE_URL
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.juicychain_env import JUICYCHAIN_API_BASE_URL
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_BATCH
from lib.juicychain_env import FUNDING_AMOUNT_CERTIFICATE
from lib.juicychain_env import FUNDING_AMOUNT_TIMESTAMPING_START
from lib.juicychain_env import FUNDING_AMOUNT_TIMESTAMPING_END
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_PATH
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

RPC = ""
URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
URL_JUICYCHAIN_API_ORGANIZATION = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION
URL_JUICYCHAIN_API_ORGANIZATION_BATCH = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_BATCH


#helper mothods
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

# test done
def connect_node():
    global RPC
    print("Connecting to: " + KOMODO_NODE + ":" + RPC_PORT)
    RPC = Proxy("http://" + RPC_USER + ":" + RPC_PASSWORD + "@" + KOMODO_NODE + ":" + RPC_PORT)
    return True


def kvupdate_wrapper(kv_key, kv_value, kv_days, kv_passphrase):
    if(type(kv_value) == type({"this":"is", "a":"json"})):
        kv_value = json.dumps(kv_value)
    txid = rpclib.kvupdate(RPC, kv_key, kv_value, kv_days, kv_passphrase)
    return txid


def kvsearch_wrapper(kv_key):
    kv_response = rpclib.kvsearch(RPC, kv_key)
    return kv_response


# test done
def sendtoaddress_wrapper(to_address, amount):
    send_amount = round(amount, 10)
    txid = rpclib.sendtoaddress(RPC, to_address, send_amount)
    return txid


# test done
def sendmany_wrapper(from_address, recipients_json):
    txid = rpclib.sendmany(RPC, from_address, recipients_json)
    return txid


# test done
def signmessage_wrapper(data):
    signed_data = rpclib.signmessage(RPC, THIS_NODE_ADDRESS, data)
    return signed_data


# test done
def housekeeping_tx():
    return sendtoaddress_wrapper(HOUSEKEEPING_ADDRESS, SCRIPT_VERSION)


# test done
def sendtoaddressWrapper(address, amount, amount_multiplier):
    print("Deprecated: use sendtoaddress_wrapper")
    send_amount = round(amount * amount_multiplier, 10)  # rounding 10??
    txid = rpclib.sendtoaddress(RPC, address, send_amount)
    return txid


# test done
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


# test done
def check_node_wallet():
    # check wallet management
    try:
        is_mine = rpclib.validateaddress(RPC, THIS_NODE_ADDRESS)['ismine']
        if is_mine is False:
            rpclib.importprivkey(RPC, THIS_NODE_WIF)
        is_mine = rpclib.validateaddress(RPC, THIS_NODE_ADDRESS)['ismine']
        return is_mine
    except Exception as e:
        print(e)
        print("## JUICYCHAIN_ERROR ##")
        print("# Node is not available. Check debug.log for details")
        print("# If node is rescanning, will take a short while")
        print("# If changing wallet & env, rescan will occur")
        print("# Exiting.")
        print("##")
        exit()


def organization_certificate_noraddress(url, org_id, THIS_NODE_ADDRESS):
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
        # url = IMPORT_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + id + "/"

        try:
            data = {"raddress": addy['address'], "pubkey": addy['pubkey']}
            res = requests.patch(url, data=data)
        except Exception as e:
            raise Exception(e)


# test done
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


# test done
def createrawtx_wrapper(txids, vouts, to_address, amount):
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


# test done
def createrawtxwithchange(txids, vouts, to_address, amount, change_address, change_amount):
    return rpclib.createrawtransactionwithchange(RPC, txids, vouts, to_address, amount, change_address, change_amount)


# test done
def createrawtx(txids, vouts, to_address, amount):
    print("Deprecated: use createrawtx_wrapper")
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


# test done
def createrawtx5(utxos_json, num_utxo, to_address, fee, change_address):
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

    to_amount = 0.00123
    change_amount = round(amount - fee - to_amount, 10)
    print("AMOUNTS: amount, to_amount, change_amount, fee")
    print(amount)
    print(to_amount)
    print(change_amount)
    print(fee)

    rawtx = createrawtxwithchange(txids, vouts, to_address, to_amount, change_address, change_amount)
    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info


# test done
def createrawtx4(utxos_json, num_utxo, to_address, fee):
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


# test done
def decoderawtx_wrapper(tx):
    return rpclib.decoderawtransaction(RPC, tx)


# test done
def decoderawtx(tx):
    print("Deprecated: use decoderawtx_wrapper(tx)")
    return rpclib.decoderawtransaction(RPC, tx)


# test done
def signtx(kmd_unsigned_tx_serialized, amounts, wif):
    txin_type, privkey, compressed = bitcoin.deserialize_privkey(wif)
    pubkey = bitcoin.public_key_from_private_key(privkey, compressed)

    jsontx = transaction.deserialize(kmd_unsigned_tx_serialized)
    inputs = jsontx.get('inputs')
    outputs = jsontx.get('outputs')
    locktime = jsontx.get('lockTime', 0)
    outputs_formatted = []
    print("\n###### IN SIGNTX FUNCTION #####\n")
    print(jsontx)
    print(inputs)
    print(outputs)
    print(locktime)

    for txout in outputs:
        outputs_formatted.append([txout['type'], txout['address'], (txout['value'])])
        print("Value of out before miner fee: " + str(txout['value']))
        print("Value of out: " + str(txout['value']))

    print("\nOutputs formatted:\n")
    print(outputs_formatted)

    for txin in inputs:
        txin['type'] = txin_type
        txin['x_pubkeys'] = [pubkey]
        txin['pubkeys'] = [pubkey]
        txin['signatures'] = [None]
        txin['num_sig'] = 1
        txin['address'] = bitcoin.address_from_private_key(wif)
        txin['value'] = amounts[inputs.index(txin)]  # required for preimage calc

    tx = Transaction.from_io(inputs, outputs_formatted, locktime=locktime)
    print("### TX before signing###")
    print(tx)
    print("### END TX ###")
    tx.sign({pubkey: (privkey, compressed)})

    print("\nSigned tx:\n")
    print(tx.serialize())
    print("Return from signtx")
    return tx.serialize()


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


# test done
def gen_wallet(data, label='NoLabelOK'):
    print("Creating a %s address signing with %s and data %s" % (label, THIS_NODE_ADDRESS, data))
    signed_data = rpclib.signmessage(RPC, THIS_NODE_ADDRESS, data)
    print("Signed data is %s" % (signed_data))
    new_wallet_json = subprocess.getoutput("php genwallet.php " + signed_data)
    print("Created wallet %s" % (new_wallet_json))

    new_wallet = json.loads(new_wallet_json)

    return new_wallet


# test done
def offlineWalletGenerator_fromObjectData_certificate(objectData):
    obj = {
        "issuer": objectData['issuer'],
        "issue_date": objectData['date_issue'],
        "expiry_date": objectData['date_expiry'],
        "identfier": objectData['identifier']
    }
    raw_json = json.dumps(obj)
    print("libjuicychain->offlineWalletGenerator object data as json: " + raw_json)

    log_label = objectData['identifier']
    offline_wallet = gen_wallet(raw_json, log_label)

    return offline_wallet


# test done
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


# test done
def get_batches_no_timestamp():
    print("10009 start import api - raw/refresco")
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

    print("New batch requires timestamping: " + str(len(batches_no_timestamp)))
    return batches_no_timestamp


# has test
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


# has test function
def get_certificates_no_timestamp():
    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS
    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(e)

    certs_no_addy = json.loads(res.text)
    return certs_no_addy


def fund_certificate(certificate_address):
    txid = sendtoaddress_wrapper(certificate_address, FUNDING_AMOUNT_CERTIFICATE)
    return txid


# test done
def postWrapper(url, data):
    res = requests.post(url, data=data)
    if(res.status_code == 200 | res.status_code == 201):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


# test done
def putWrapper(url, data):
    res = requests.put(url, data=data)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


# has test function
def patchWrapper(url, data):
    res = requests.patch(url, data=data)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


# has test function
def getWrapper(url):
    res = requests.get(url)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


# test done
def get_jcapi_organization():
    print("GET juicychain-api organization query: " + URL_JUICYCHAIN_API_ORGANIZATION + "?raddress=" + THIS_NODE_ADDRESS)
    res = getWrapper(URL_JUICYCHAIN_API_ORGANIZATION + "?raddress=" + THIS_NODE_ADDRESS)
    print(res)
    organizations = json.loads(res)
    # TODO E721 do not compare types, use "isinstance()" pep8
    if type(organizations) == type(['d', 'f']):
        return organizations[0]
    return organizations


# test done
def batch_wallets_generate_timestamping(batchObj, import_id):
    json_batch = json.dumps(batchObj)
    # anfp_wallet = gen_wallet(json_batch['anfp'], "anfp")
    # pon_wallet = gen_wallet(json_batch['pon'], "pon")
    bnfp_wallet = gen_wallet(batchObj['bnfp'], "bnfp")
    # pds_wallet = juicychain.gen_wallet(data['pds'], "pds")
    # jds_wallet = juicychain.gen_wallet(data['jds'], "jds")
    # jde_wallet = juicychain.gen_wallet(data['jde'], "jde")
    # bbd_wallet = juicychain.gen_wallet(data['bbd'], "bbd")
    # pc_wallet = juicychain.gen_wallet(data['pc'], "pc")
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


# test done
def batch_wallets_timestamping_update(batch_integrity):
    batch_integrity_url = URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + batch_integrity['id'] + "/"
    print(batch_integrity)
    batch_integrity_response = putWrapper(batch_integrity_url, batch_integrity)
    return batch_integrity_response


# test done
def batch_wallets_timestamping_start(batch_integrity, start_txid):
    batch_integrity_url = URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + batch_integrity['id'] + "/"
    print(batch_integrity)
    batch_integrity['integrity_pre_tx'] = start_txid
    print(batch_integrity)
    # data = {'name': 'chris', 'integrity_address': integrity_address[
    #    'address'], 'integrity_pre_tx': integrity_start_txid, 'batch_lot_raddress': bnfp_wallet['address']}

    batch_integrity_start_response = putWrapper(batch_integrity_url, batch_integrity)
    return batch_integrity_start_response


# test done
def batch_wallets_timestamping_end(batch_integrity, end_txid):
    batch_integrity['integrity_post_tx'] = end_txid
    print(batch_integrity)
    batch_integrity_end_response = batch_wallets_timestamping_update(batch_integrity)
    return batch_integrity_end_response


# test done
def batch_wallets_fund_integrity_start(integrity_address):
    return sendtoaddress_wrapper(integrity_address, FUNDING_AMOUNT_TIMESTAMPING_START)


# test done
def batch_wallets_fund_integrity_end(integrity_address):
    return sendtoaddress_wrapper(integrity_address, FUNDING_AMOUNT_TIMESTAMPING_END)


def organization_send_batch_links(batch_integrity):
    sample_pool_po = "RWSVFtCJfRH5ErsXJCaz9YNVKx7PijxpoV"
    sample_pool_batch_lot = "R9X5CBJjmVmJe4a533hemBf6vCW2m3BAqH"
    print("MAIN WALLET " + THIS_NODE_ADDRESS + " SENDMANY TO BATCH_LOT (bnfp), POOL_PO (pon), POOL_BATCH_LOT")
    json_object = {sample_pool_po: SCRIPT_VERSION,
                   sample_pool_batch_lot: SCRIPT_VERSION,
                   batch_integrity['batch_lot_raddress']: SCRIPT_VERSION
                   }
    sendmany_txid = sendmany_wrapper(THIS_NODE_ADDRESS, json_object)
    return sendmany_txid


def timestamping_save_batch_links(id, sendmany_txid):
    print("** txid ** (Main org wallet sendmany BATCH_LOT/POOL_PO/GTIN): " + sendmany_txid)
    tstx_data = {'sender_raddress': THIS_NODE_ADDRESS,
                 'tsintegrity': id, 'sender_name': 'ORG WALLET', 'txid': sendmany_txid}
    ts_response = postWrapper(URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH, tstx_data)
    print("POST ts_response: " + ts_response)
    return ts_response


def timestamping_save_certificate(id, sender_name, sender_wallet, certificate_txid):
    print("** txid ** (Certificate to batch_lot): " + certificate_txid)
    tstx_data = {'sender_raddress': sender_wallet['address'],
                 'tsintegrity': id, 'sender_name': sender_name, 'txid': certificate_txid}
    print(tstx_data)
    ts_response = postWrapper(URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH, tstx_data)
    print("POST ts_response: " + ts_response)
    return ts_response


# test done
def get_certificate_for_test(url):
    return getWrapper(url)


# test done
def get_certificate_for_batch():
    test_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "8/"
    certificate = json.loads(get_certificate_for_test(test_url))
    return certificate


def push_batch_data_consumer(jcapi_org_id, batch, batch_wallet):
        data = {'identifier': batch['bnfp'],
                'jds': batch['jds'],
                'jde': batch['jde'],
                'date_production_start': batch['pds'],
                'date_best_before': batch['bbd'],
                'origin_country': batch['pc'],
                'raddress': batch_wallet['address'],
                'pubkey': batch_wallet['pubkey'],
                'organization': jcapi_org_id}
        jcapi_response = postWrapper(URL_JUICYCHAIN_API_ORGANIZATION_BATCH, data=data)
        jcapi_batch_id = json.loads(jcapi_response)['id']
        print("BATCH ID @ JUICYCHAIN-API: " + str(jcapi_batch_id))
        return jcapi_response
