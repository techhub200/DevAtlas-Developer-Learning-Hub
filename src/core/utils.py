from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def generate_hashed_password(password: str):
    # Your current environment has passlib+bcrypt mismatch (bcrypt lacks __about__). 
    # Avoid passlib entirely by using bcrypt directly.
    import bcrypt

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):
    import bcrypt

    plain_bytes = plain_password.encode("utf-8")
    if len(plain_bytes) > 72:
        plain_bytes = plain_bytes[:72]

    return bcrypt.checkpw(plain_bytes, hashed_password.encode("utf-8"))





