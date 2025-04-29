# tests/test_verify_endpoint.py

# Kein File mitgegeben
def test_verify_no_file(client):
    res = client.post("/api/verify", data={}, content_type="multipart/form-data")
    assert res.status_code == 400
    assert res.get_json() == {"error": "No file provided"}

# File nicht notariell hinterlegt
def test_verify_not_notarized(client):
    from tests.conftest import make_data
    data = make_data(b"Unbekannt", "dummy")
    data.pop("documentId")
    res = client.post("/api/verify", data=data, content_type="multipart/form-data")
    assert res.status_code == 404
    assert res.get_json() == {"verified": False}

# Nach erfolgreicher Notarisierung verifizieren
def test_verify_after_notarize(client):
    from tests.conftest import make_data
    # Erst notarisieren
    data = make_data(b"Inhalt", "workerZ")
    res_not = client.post("/api/notarize", data=data, content_type="multipart/form-data")
    assert res_not.status_code == 200

    # Dann verifizieren (documentId wird ignoriert)
    data_v = make_data(b"Inhalt", "workerZ")
    data_v.pop("documentId")
    res_ver = client.post("/api/verify", data=data_v, content_type="multipart/form-data")
    assert res_ver.status_code == 200
    json_data = res_ver.get_json()
    assert json_data.get("verified") is True
    assert json_data.get("timestamp") > 0
