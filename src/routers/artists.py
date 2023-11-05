from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from .. import crud
from ..dependencies import get_db
from ..util import album_to_playlist_item, has_tracks, track_to_playlist_item

router = APIRouter()


@router.get("/{artist_id}.m3u")
def get_artist_playlist(
    artist_id: UUID, request: Request, db: Session = Depends(get_db)
):
    albums = crud.get_artist_albums(db, artist_id)
    filtered_albums = filter(has_tracks, albums)
    tracks = crud.get_artist_tracks_without_album(db, artist_id)
    data = "\n".join(
        [
            "#EXTM3U",
            "\n".join(
                [album_to_playlist_item(request, album) for album in filtered_albums]
            ),
            "\n".join([track_to_playlist_item(request, track) for track in tracks]),
        ]
    )
    return Response(content=data, media_type="audio/x-mpegurl")
