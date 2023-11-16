from unittest.mock import Mock
from uuid import UUID, uuid4

from fastapi.datastructures import URL

from pytunes import models
from pytunes.util import sha1_to_uuid, track_to_playlist_item


def test_sha1_to_uuid():
    assert sha1_to_uuid("0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33") == UUID(
        "0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2"
    )


def test_track_to_playlist_item():
    track_id = uuid4()
    track_name = "foo"
    artist_name = "bar"
    track = models.Track(
        id=track_id, name=track_name, artists=[models.Artist(name=artist_name)]
    )
    track_url = f"http://testserver/tracks/{track_id}.m3u8"
    mock_request = Mock()
    mock_request.url_for = Mock(return_value=URL(track_url))

    playlist_item = track_to_playlist_item(mock_request, track)

    assert playlist_item == "\n".join(
        [f"#EXTINF:-1,{artist_name} - {track_name}", track_url]
    )
