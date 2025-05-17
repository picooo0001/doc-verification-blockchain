# backend/app/web3utils.py
import os
import json
from .models import Organization
from web3 import Web3, HTTPProvider
from .config import Config

with open(Config.CONTRACT_ABI_PATH) as f:
    NOTARY_ABI = json.load(f)['abi']

RPC_URL = os.getenv("RPC_URL")
if not RPC_URL:
    raise RuntimeError("Es ist keine RPC_URL in der Umgebung gesetzt.")

w3 = Web3(HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise RuntimeError(f"Kann keine Verbindung zu Ethereum-Node herstellen unter {RPC_URL}")

# Pfad zu deinem Hardhat-Artifact:
# projectroot/contracts/artifacts/contracts/Notary.sol/Notary.json
HERE = os.path.dirname(__file__)
ARTIFACT_PATH = os.path.abspath(
    os.path.join(
        HERE,
        '..',    # backend/app → backend
        '..',    # backend → projectroot
        'contracts',
        'artifacts',
        'contracts',
        'Notary.sol',
        'Notary.json'
    )
)

def get_notary_contract_for_org(org_or_address):
    if isinstance(org_or_address, Organization):
        ca = org_or_address.contract_address
    else:
        ca = org_or_address

    if not ca:
        raise RuntimeError("Kein Contract hinterlegt für diese Organisation")

    checksum_addr = Web3.to_checksum_address(ca)
    return w3.eth.contract(address=checksum_addr, abi=NOTARY_ABI)
