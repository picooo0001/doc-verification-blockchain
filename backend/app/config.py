import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CONTRACT_ABI_PATH = os.getenv("CONTRACT_ABI_PATH")
    if not CONTRACT_ABI_PATH:
        raise RuntimeError("Environment variable CONTRACT_ABI_PATH is not set")

    RPC_URL = os.getenv("RPC_URL")
    if not RPC_URL:
        raise RuntimeError("Environment variable RPC_URL is not set")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("Environment variable SQLALCHEMY_DATABASE_URI is not set")

    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("Environment variable SECRET_KEY is not set")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
