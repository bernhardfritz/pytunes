from uuid import uuid4

from pytunes.testing.setup import client


def test_get_track_playlist(fs):
    track_id = uuid4()
    fs.create_file(f"/data/.pytunes/{track_id}.m3u8")

    response = client.get(f"/tracks/{track_id}.m3u8")

    assert response.status_code == 200


def test_get_track_segment(fs):
    track_id = uuid4()
    fs.create_file(f"/data/.pytunes/{track_id}.0.m4a")

    response = client.get(f"/tracks/{track_id}.0.m4a")

    assert response.status_code == 200
