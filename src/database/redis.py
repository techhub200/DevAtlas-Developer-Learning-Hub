import redis
import time
from datetime import datetime
from src.core.config import REDIS_HOST,REDIS_PORT

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

def _access_token_blacklist_key(jti: str) -> str:
    return f"key:{jti}" 

def add_access_token_to_blacklist(jti: str, exp: datetime) -> None:
   
    key = _access_token_blacklist_key(jti)
    now_ts = time.time()
    exp_ts = exp.timestamp()
    ttl_seconds = max(0, int(exp_ts - now_ts))
    r.set(key, True, ex=ttl_seconds)


def is_access_token_blacklisted(jti: str) -> bool:
    key = _access_token_blacklist_key(jti)
    try:
        if r.exists(key):
            return True
        return False
    except redis.exceptions.RedisError as e:
        print(f"[Redis] blacklist check failed for jti={jti}")
        return False