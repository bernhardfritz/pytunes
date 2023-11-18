from unittest.mock import patch
from uuid import uuid4

from pytunes import models
from pytunes.testing.setup import client


@patch(
    "pytunes.routers.artists.crud.get_artist_albums",
    return_value=[
        models.Album(
            name="album_name_1", tracks=[models.Track(id=uuid4(), name="track_name_1")]
        ),
        models.Album(
            name="album_name_2", tracks=[models.Track(id=uuid4(), name="track_name_1")]
        ),
    ],
)
@patch("pytunes.routers.artists.crud.get_artist_tracks_without_album", return_value=[])
@patch("pytunes.routers.artists.album_to_playlist_item", return_value="playlist_item")
def test_get_artist_playlist(
    mock_get_artist_albums,
    mock_get_artist_tracks_without_album,
    mock_album_to_playlist_item,
):
    artist_id = uuid4()

    response = client.get(f"/artists/{artist_id}.m3u")

    assert response.status_code == 200
    assert response.text == "\n".join(["#EXTM3U", "playlist_item", "playlist_item"])
    assert response.headers["content-type"] == "audio/x-mpegurl"
