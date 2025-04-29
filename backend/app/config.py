import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Lokaler Hardhat RPC
    RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
    # Pfad zur Datei mit der deployed contract address
    DEPLOYED_ADDRESS_FILE = os.getenv(
        "DEPLOYED_ADDRESS_FILE",
        "../contracts/contracts/deployed-address.txt"
    )
    # Contract ABI – wird später von web3utils geladen
    CONTRACT_ABI_PATH = os.getenv(
        "CONTRACT_ABI_PATH",
        "../contracts/artifacts/contracts/Notary.sol/Notary.json"
    )
    # Datenbank URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://myuser:mypass@localhost:5432/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "setz-dir-ein-geheimes-key")

