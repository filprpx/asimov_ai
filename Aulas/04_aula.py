import openai, os
from dotenv import load_dotenv

load_dotenv(override=True)

# Looks for the env variable OPENAI_API_KEY
client = openai.Client()