#test_notarize_id_has.py

# Kein File mitgegeben
def test_notarize_no_file(client):
    res = client.post("/api/notarize",
                      data={"documentId": "worker1"},
                      content_type="multipart/form-data")
    assert res.status_code == 400
    assert res.get_json() == {"error": "No file provided"}

# Keine ID mitgegeben
def test_notarize_no_id(client):
    from tests.conftest import make_data
    data = make_data(b"", "", "empty.pdf")
    # remove documentId to simulate missing ID
    data.pop("documentId")
    res = client.post("/api/notarize", data=data,
                      content_type="multipart/form-data")
    assert res.status_code == 400
    assert res.get_json() == {"error": "No documentId provided"}

def test_first_notarize_ok(client):
    from tests.conftest import make_data
    data = make_data(b"Version1", "worker1")
    res = client.post("/api/notarize", data=data, content_type="multipart/form-data")
    assert res.status_code == 200

def test_duplicate_same_id_same_file(client):
    from tests.conftest import make_data
    data = make_data(b"VersionX", "workerX")
    assert client.post("/api/notarize", data=data, content_type="multipart/form-data").status_code == 200
    # nochmal dasselbe
    res2 = client.post("/api/notarize", data=make_data(b"VersionX", "workerX"), content_type="multipart/form-data")
    assert res2.status_code == 400
    assert "Schon notariell" in res2.get_json()["error"]

def test_diff_file_same_id_forbidden(client):
    from tests.conftest import make_data
    data = make_data(b"Orig", "workerY")
    assert client.post("/api/notarize", data=data, content_type="multipart/form-data").status_code == 200
    # andere Datei, gleiche ID → verboten
    res2 = client.post("/api/notarize", data=make_data(b"Mod", "workerY"), content_type="multipart/form-data")
    assert res2.status_code == 400
    assert res2.get_json()["error"] == "Dokument darf nicht geändert werden"

def test_same_file_diff_id_allowed(client):
    from tests.conftest import make_data
    data1 = make_data(b"Common", "workerA")
    data2 = make_data(b"Common", "workerB")
    assert client.post("/api/notarize", data=data1, content_type="multipart/form-data").status_code == 200
    assert client.post("/api/notarize", data=data2, content_type="multipart/form-data").status_code == 200
