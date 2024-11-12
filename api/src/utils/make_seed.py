import hashlib
from typing import Any


def make_seed(params: Any) -> int:
    hash_object = hashlib.sha256(str(params).encode())
    hash_hex = hash_object.hexdigest()
    seed = int(hash_hex[:8], 16)

    return seed & 0xFFFFFFFF


def get_hash(params: Any, prefix: str | None = None) -> str:
    params_str = str(params)
    hash_object = hashlib.sha256(params_str.encode())
    value = hash_object.hexdigest()

    return f"{prefix}:{value}" if prefix else value
