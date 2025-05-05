from .config import Config
from web3 import Web3
from .models import Organization
import json

# Web3-Provider
w3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
if not w3.is_connected():
    raise ConnectionError(f"Cannot connect to {Config.RPC_URL}")

# Contract-Adresse aus Datei (einmalig) + Checksum
with open(Config.DEPLOYED_ADDRESS_FILE) as f:
    raw_addr = f.read().strip()
contract_address = Web3.to_checksum_address(raw_addr)

# Contract-ABI laden
with open(Config.CONTRACT_ABI_PATH) as f:
    contract_abi = json.load(f)["abi"]

# Contract-Instanz
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
#Debugging: print(f"[web3utils] Contract loaded at address: {contract.address}")

# Default-Sender (Hardhat unlocked account)
default_sender_account = w3.eth.accounts[2]

def get_user_org_address(user):
    """
    Liefert die on-chain Adresse (chain_address) der Organisation,
    der der gegebene Flask-User zugeordnet ist.
    """
    org = Organization.query.get(user.organization_id)
    return org.chain_address