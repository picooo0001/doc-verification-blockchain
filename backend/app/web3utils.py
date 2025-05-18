# backend/app/web3utils.py
import os
import json
from .models import Organization
from web3 import Web3, HTTPProvider
from .config import Config

with open(Config.CONTRACT_ABI_PATH, 'r') as f:
    try:
        NOTARY_ABI = json.load(f)['abi']
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Fehler beim Laden des ABI von {Config.CONTRACT_ABI_PATH}: {e}")

w3 = Web3(HTTPProvider(Config.RPC_URL))
if not w3.is_connected():
    raise RuntimeError(f"Kann keine Verbindung zum Ethereum-Node herstellen: {Config.RPC_URL}")

ARTIFACT_PATH = os.getenv('ARTIFACT_PATH')
if not ARTIFACT_PATH:
    here = os.path.dirname(__file__)
    ARTIFACT_PATH = os.path.abspath(
        os.path.join(here, '..', '..', 'contracts', 'artifacts',
                     'contracts', 'Notary.sol', 'Notary.json')
    )
if not os.path.isfile(ARTIFACT_PATH):
    raise RuntimeError(f"Artifact-Datei nicht gefunden unter: {ARTIFACT_PATH}")

def get_notary_contract_for_org(org_or_address):
    """
    Liefert eine Web3-Contract-Instanz für den Notary-Smart-Contract einer Organisation.

    Akzeptiert entweder ein Organization-Objekt oder direkt eine Contract-Adresse.
    Validiert, dass eine Adresse vorliegt, wandelt sie in eine checksummierte Form um
    und gibt das Contract-Objekt basierend auf dem vordefinierten NOTARY_ABI zurück.

    :param org_or_address: Organisation oder Contract-Adresse der Notary-Instanz
    :type org_or_address: Organization | str
    :raises RuntimeError: Wenn keine Contract-Adresse hinterlegt ist
    :return: Web3 Contract-Instanz für den Notary-Contract
    :rtype: web3.contract.Contract
    """
    if isinstance(org_or_address, Organization):
        ca = org_or_address.contract_address
    else:
        ca = org_or_address

    if not ca:
        raise RuntimeError("Kein Contract hinterlegt für diese Organisation")

    checksum_addr = Web3.to_checksum_address(ca)
    return w3.eth.contract(address=checksum_addr, abi=NOTARY_ABI)
