from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from .. import crud
from ..dependencies import get_db
from ..util import track_to_playlist_item

router = APIRouter()


@router.get("/{album_id}.m3u")
def get_album_playlist(album_id: UUID, request: Request, db: Session = Depends(get_db)):
    tracks = crud.get_album_tracks(db, album_id)
    data = "\n".join(
        filter(
            bool,
            [
                "#EXTM3U",
                "\n".join([track_to_playlist_item(request, track) for track in tracks]),
            ],
        )
    )
    return Response(content=data, media_type="audio/x-mpegurl")
