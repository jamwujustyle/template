import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="server/.env")
name = os.environ.get("DB_NAME")

print(name)
