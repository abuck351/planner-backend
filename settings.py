import os
from dotenv import load_dotenv


load_dotenv(verbose=True)

DB_URI = os.getenv("DB_URI")
PLANNER_SECRET_KEY = os.getenv("PLANNER_SECRET_KEY")
