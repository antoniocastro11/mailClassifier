import os 
from dotenv import load_dotenv

load_dotenv()

OPENAPI_KEY = os.getenv()("OPENAPI_KEY")