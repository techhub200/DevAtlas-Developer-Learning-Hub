from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET_KEY=os.get("JWT_SECRET_KEY")
JWT_ALGORITHM=os.get("JWT_ALGORITHM")

