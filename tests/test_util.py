from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest
from fastapi.datastructures import URL

from pytunes import models
from pytunes.util import (
    album_to_playlist_item,
    has_tracks,
    sha1_to_uuid,
    track_to_playlist_item,
)


def test_sha1_to_uuid():
    assert sha1_to_uuid("0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33") == UUID(
        "0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2"
    )


def test_track_to_playlist_item():
    track = models.Track(
        id=uuid4(), name="track_name", artists=[models.Artist(name="artist_name")]
    )
    track_url = f"http://testserver/tracks/{track.id}.m3u8"
    mock_request = Mock()
    mock_request.url_for = Mock(return_value=URL(track_url))

    playlist_item = track_to_playlist_item(mock_request, track)

    assert playlist_item == "\n".join(
        ["#EXTINF:-1,artist_name - track_name", track_url]
    )


def test_album_to_playlist_item():
    album = models.Album(name="album_name")
    album_url = f"http://testserver/album/{album.id}.m3u"
    mock_request = Mock()
    mock_request.url_for = Mock(return_value=URL(album_url))

    playlist_item = album_to_playlist_item(mock_request, album)

    assert playlist_item == "\n".join(["#EXTINF:-1,album_name", album_url])


@pytest.mark.parametrize(
    "artistOrAlbum,expected",
    [
        (models.Artist(name="artist_name"), False),
        (
            models.Artist(
                name="artist_name", tracks=[models.Track(id=uuid4(), name="track_name")]
            ),
            True,
        ),
        (models.Album(name="album_name"), False),
        (
            models.Album(
                name="album_name", tracks=[models.Track(id=uuid4(), name="track_name")]
            ),
            True,
        ),
    ],
)
def test_has_tracks(artistOrAlbum, expected):
    assert has_tracks(artistOrAlbum) == expected
