from pytunes.testing.client import client


def test_get_track_playlist(fs):
    fs.create_file("/data/.pytunes/0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2.m3u8")
    response = client.get("/tracks/0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2.m3u8")
    assert response.status_code == 200


def test_get_track_segment(fs):
    fs.create_file("/data/.pytunes/0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2.0.m4a")
    response = client.get("/tracks/0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2.0.m4a")
    assert response.status_code == 200
