from unittest.mock import patch
from uuid import uuid4

from pytunes import models
from pytunes.testing.setup import client


@patch(
    "pytunes.routers.albums.crud.get_album_tracks",
    return_value=[
        models.Track(id=uuid4(), name="foo"),
        models.Track(id=uuid4(), name="bar"),
    ],
)
@patch("pytunes.routers.albums.track_to_playlist_item", return_value="playlist_item")
def test_get_album_playlist(mock_get_album_tracks, mock_track_to_playlist_item):
    album_id = uuid4()

    response = client.get(f"/albums/{album_id}.m3u")

    assert response.status_code == 200
    assert response.text == "\n".join(["#EXTM3U", "playlist_item", "playlist_item"])
    assert response.headers["content-type"] == "audio/x-mpegurl"
