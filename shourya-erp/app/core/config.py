import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shourya_erp.db")
SECRET_KEY = os.getenv("SECRET_KEY", "shourya-erp-secret-change-in-production")
APP_NAME = "Shourya Bharatgas ERP"
