import secrets
import sys

OUTPUT_TMPL ="""export SHARED_SERVER_SECRET_KEY='{server_key}'
export SHARED_SERVER_HMAC_KEY='{hmac_key}'
"""

params = {
    'server_key': secrets.token_hex(),
    'hmac_key': secrets.token_hex(),
}

sys.stdout.write(OUTPUT_TMPL.format(**params))
