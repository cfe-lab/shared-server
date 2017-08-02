import base64
import hmac
import json
import secrets
import typing

from django.conf import settings

from . import models


def _message_digest(msg: bytes) -> str:
    key = bytes(settings.HMAC_KEY, 'utf8')
    msg_hasher = hmac.new(key, msg=msg, digestmod='sha256')
    digest = msg_hasher.digest()
    enc_digest = base64.urlsafe_b64encode(digest)
    return str(enc_digest, 'utf8')
    

def _new_msg(id_code: str) -> str:
    msg_str = json.dumps({
        'c': str(id_code),
    })
    msg_bytes = bytes(msg_str, 'utf8')
    msg_enc = base64.urlsafe_b64encode(msg_bytes)    
    msg_enc_str = str(msg_enc, 'utf8')
    return msg_enc_str


def _parse_id_code(msg_enc_str: str) -> typing.Optional[str]:
    '''Parse the id_code from an encoded message.

    ONLY USE THIS FUNCTION ON A VERIFIED TOKEN. It might have decoding
    vulnerabilities.
    '''
    try:
        msg_enc_bytes = bytes(msg_enc_str, 'utf8')
        msg_bytes = base64.urlsafe_b64decode(msg_enc_bytes)
        msg_str = str(msg_bytes, 'utf8')
        msg = json.loads(msg_str)
        id_code = msg.get('c', None)
        return id_code
    except Exception as e:
        return None


def validate_and_parse_id_code(token: str) -> typing.Optional[str]:
    try:
        msg, msg_digest = token.split('.', 1)
        clean_msg_digest = _message_digest(bytes(msg, 'utf8'))
        if not hmac.compare_digest(msg_digest, clean_msg_digest):
            return None
        else:
            return _parse_id_code(msg)
    except Exception as e:
        print(e)
        # TODO(nknight): log the exception?
        return None


def new(id_code: str) -> str:
    msg = _new_msg(id_code)
    digest = _message_digest(bytes(msg, 'utf8'))
    return "{}.{}".format(msg, digest)
