from dotenv import load_dotenv
import os

load_dotenv()

print("Loaded URL:", os.getenv("CLEAN_DATA_URL"))