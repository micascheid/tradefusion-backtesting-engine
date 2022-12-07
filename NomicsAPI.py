import os
from nomics import Nomics
from dotenv import load_dotenv

# load_dotenv()
API_KEY = os.getenv('API_KEY')
API = Nomics(API_KEY)