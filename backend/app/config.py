# backend/app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Pfad zum ABI des Notary-Vertrags
    CONTRACT_ABI_PATH = os.getenv(
        "CONTRACT_ABI_PATH",
        "../contracts/artifacts/contracts/Notary.sol/Notary.json"
    )

    # Datenbank URL
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://"
        "postgres.fffabyazqvvwdaimdcmk:"
        "qE9b%5EM%3B42%3BLn"
        "@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "setz-dir-ein-geheimes-key")
