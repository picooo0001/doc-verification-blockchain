# backend/app/web3utils.py

from web3 import Web3
import json
import os
from .config import Config
from .models import Organization

# Web3-Provider
w3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
if not w3.is_connected():
    raise ConnectionError(f"Cannot connect to {Config.RPC_URL}")

# ABI des Notary-Vertrags laden (einmalig)
abi_path = Config.CONTRACT_ABI_PATH
if not os.path.isabs(abi_path):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    abi_path = os.path.join(base_dir, abi_path)

with open(abi_path, 'r') as f:
    artifact = json.load(f)
    NOTARY_ABI = artifact.get("abi", artifact)

# Default-Sender (Hardhat unlocked account)
default_sender_account = w3.eth.accounts[2]

def get_notary_contract_for_address(address: str):
    """
    Gibt eine Contract-Instanz des Notary-Vertrags für die gegebene Adresse zurück.
    Wirft einen Fehler, wenn keine Adresse übergeben wird.
    """
    if not address:
        raise ValueError("Keine Smart-Contract-Adresse für die Organisation gesetzt")
    checksum = Web3.to_checksum_address(address)
    return w3.eth.contract(address=checksum, abi=NOTARY_ABI)

def get_notary_contract_for_org(org):
    """
    Gibt die Contract-Instanz für die angegebene Organisation zurück.
    """
    return get_notary_contract_for_address(org.contract_address)

def get_user_org_address(user):
    """
    Liefert die on-chain Wallet-Adresse der Organisation, der der gegebene User zugeordnet ist.
    """
    org = Organization.query.get(user.organization_id)
    if not org or not org.chain_address:
        raise ValueError("Organisation hat keine chain_address hinterlegt")
    return org.chain_address
