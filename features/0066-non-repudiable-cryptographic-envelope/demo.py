import json
import logging
import time
import base64
import sys
from typing import Optional

from indy import crypto, did, ledger, pool, wallet
from indy.error import ErrorCode, IndyError
from src.utils import get_pool_genesis_txn_path, run_coroutine, PROTOCOL_VERSION


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def run():
    sender_wallet_config = json.dumps({"id": "sender_wallet"})
    sender_wallet_credentials = json.dumps({"key": "sender_wallet_key"})

    receiver_wallet_config = json.dumps({"id": "receiver_wallet"})
    receiver_wallet_credentials = json.dumps({"key": "receiver_wallet_key"})

    # Delete old wallet if it still exists from last run and create a new one
    try:
        await wallet.delete_wallet(sender_wallet_config, sender_wallet_credentials)
        await wallet.delete_wallet(receiver_wallet_config, receiver_wallet_credentials)
    except IndyError as ex:
        pass

    # Setup sender and receiver wallet with statically generated key based on seed
    await wallet.create_wallet(sender_wallet_config, sender_wallet_credentials)
    await wallet.create_wallet(receiver_wallet_config, receiver_wallet_credentials)
    sender_wallet_handle = await wallet.open_wallet(sender_wallet_config, sender_wallet_credentials)
    receiver_wallet_handle = await wallet.open_wallet(receiver_wallet_config, receiver_wallet_credentials)
    sender_did_info = {'seed': '0000000000000000000000000Sender1'}
    receiver_did_info = {'seed': '00000000000000000000000Receiver1'}
    (sender_did, sender_key) = await did.create_and_store_my_did(sender_wallet_handle, json.dumps(sender_did_info))
    (receiver_did, receiver_key) = await did.create_and_store_my_did(receiver_wallet_handle, json.dumps(receiver_did_info))
    logger.info("verkey:" + sender_key)

    # Build jose_header
    jose_header = {}
    jose_header['alg'] = "edDSA"
    jose_header['kid'] = sender_key
    jose_string = json.dumps(jose_header)
    jose_bytes = str.encode(jose_string)

    logger.info("JOSE Header:" + jose_string)

    # build payload json structure
    payload = {}
    payload['@id'] = "123456780"
    payload['@type'] = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message"
    payload['~l10n'] = {"locale": "en"}
    payload['sent_time'] = "2019-01-15 18:42:01Z"
    payload['content'] = "Your hovercraft is full of eels."
    payload_str = json.dumps(payload)
    payload_bytes = str.encode(payload_str)

    logger.info("Payload: " + payload_str)

    # combine payloads base64URL encode

    b64_jose = base64.urlsafe_b64encode(jose_bytes).decode('utf-8')
    b64_payload = base64.urlsafe_b64encode(payload_bytes).decode('utf-8')
    msg_data_as_str = b64_jose + "." + b64_payload

    logger.info("Message data to be signed: " + msg_data_as_str)

    # sign bytes
    sig_bytes = await crypto.crypto_sign(sender_wallet_handle, sender_key, str.encode(msg_data_as_str))
    signature = base64.urlsafe_b64encode(sig_bytes).decode('utf-8')
    logger.info("signature: " + signature)

    # Concatenate signature
    jws = msg_data_as_str + "." + signature

    logger.info("JWS: " + jws)

    # Encrypt with Pack msg
    packed_msg = await crypto.pack_message(sender_wallet_handle, jws, [receiver_key], sender_key)

    logger.info("Packed Message Size: " + str(sys.getsizeof(packed_msg)))
    logger.info("Packed Message: " + packed_msg.decode('utf-8'))

    # Decrypt with unpack msg
    unpacked_bytes = await crypto.unpack_message(receiver_wallet_handle, packed_msg)
    unpacked_str = unpacked_bytes.decode("utf-8")
    unpacked_output = json.loads(unpacked_str)

    logger.info("Unpacked Message: " + unpacked_str)

    # verify JWS
    unpacked_jws = unpacked_output['message']
    split_signed_data = unpacked_jws.rsplit('.', 1)

    payload_to_verify = split_signed_data[0]
    sig_to_verify = split_signed_data[1]

    logger.info("Payload to verify: " + payload_to_verify)
    logger.info("Signature to verify: " + sig_to_verify)

    verified = await crypto.crypto_verify(unpacked_output["sender_verkey"], str.encode(payload_to_verify),
                                          base64.urlsafe_b64decode(str.encode(sig_to_verify)))

    # Show original message
    b64_message_split = unpacked_jws.split('.')
    message = base64.urlsafe_b64decode(b64_message_split[1]).decode('utf-8')
    logger.info("Original Message: " + message)

if __name__ == '__main__':
    run_coroutine(run)
    time.sleep(1)  # FIXME waiting for libindy thread complete
