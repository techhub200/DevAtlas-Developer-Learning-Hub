
from src.api.config import JWT_ALGORITHM,JWT_SECRET_KEY
import jwt 
from datetime import timedelta,datetime
from fastapi import HTTPException,status 


def create_json_web_token(token_type:str,user_details:dict ,expiry:timedelta):
 payload = {
        "type": token_type,
        "user": user_details,
        "exp": datetime.utcnow() + expiry,
    }
 return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def create_access_token(user:dict,current_time:timedelta):
   return create_json_web_token("Access",user,current_time)


def create_refresh_token(user:dict,current_time:timedelta):
   return create_json_web_token("Access",user,current_time)


def decode_token(token:str):
 try:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
 except:
    raise HTTPException(status=status.HTTP_417_EXPECTATION_FAILED,detail="Token Not decode")
 

def decode_access_token(token:str):
   payload= decode_token(token)
   if payload.get("type") != "access":
        raise Exception("Invalid token type")

   return payload


def decode_refresh_token(token:str):
   payload= decode_token(token)
   if payload.get("type") != "refresh":
        raise Exception("Invalid token type")

   return payload