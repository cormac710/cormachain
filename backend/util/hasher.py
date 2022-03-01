import hashlib


import json


def hasher(*data):
    """
    return sha-265 hash of data
    """
    stringified = sorted(
        map(
            lambda args: json.dumps(args), data
        )
    )
    return hashlib.sha256(
        ''.join(stringified).encode('utf-8')
    ).hexdigest()
