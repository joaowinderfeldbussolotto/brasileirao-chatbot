from dotenv import load_dotenv
import os
load_dotenv()

class Settings():
    API_URL = os.getenv('API_URL')

settings = Settings()