import os
import json
from dotenv import load_dotenv


config = None


load_dotenv()
with open('config.json', 'r') as f:
    config = json.load(f)
if config['key'] is None:
    config['key'] = os.environ['key']
if config['secret'] is None:
    config['secret'] = os.environ['secret']

