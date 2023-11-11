from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.apache import HtpasswdFile
from redis import Redis
from sqlalchemy.orm import Session

from . import crud
from .dependencies import get_db, get_ht, get_store
from .routers import albums, artists, tracks
from .util import artist_to_playlist_item, has_tracks, track_to_playlist_item

SESSION_ID_KEY = "pytunes_session_id"
SESSION_STORE_KEY_PREFIX = f"{SESSION_ID_KEY}:"
SESSION_TIMEOUT = 3600

app = FastAPI()

security = HTTPBasic()


def get_session_id(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    ht: HtpasswdFile = Depends(get_ht),
    store: Redis = Depends(get_store),
):
    if not ht.check_password(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_id = token_urlsafe(16)
    store.set(
        f"{SESSION_STORE_KEY_PREFIX}{session_id}", credentials.username, SESSION_TIMEOUT
    )
    return session_id


def get_current_username(request: Request, store: Redis = Depends(get_store)):
    session_id = request.cookies.get(SESSION_ID_KEY)
    if (
        session_id is None
        or (username := store.get(f"{SESSION_STORE_KEY_PREFIX}{session_id}")) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username


@app.get("/")
def get_root(session_id: Annotated[str, Depends(get_session_id)]):
    response = RedirectResponse("index.m3u")
    response.set_cookie(SESSION_ID_KEY, session_id, SESSION_TIMEOUT)
    return response


@app.get("/index.m3u")
def get_index_playlist(
    request: Request,
    username: Annotated[str, Depends(get_current_username)],
    db: Session = Depends(get_db),
):
    artists = crud.get_artists(db)
    filtered_artists = filter(has_tracks, artists)
    tracks = crud.get_tracks_without_artists(db)
    data = "\n".join(
        [
            "#EXTM3U",
            "\n".join(
                [
                    artist_to_playlist_item(request, artist)
                    for artist in filtered_artists
                ]
            ),
            "\n".join([track_to_playlist_item(request, track) for track in tracks]),
        ]
    )
    return Response(content=data, media_type="audio/x-mpegurl")


app.include_router(
    albums.router, prefix="/albums", dependencies=[Depends(get_current_username)]
)
app.include_router(
    artists.router, prefix="/artists", dependencies=[Depends(get_current_username)]
)
app.include_router(
    tracks.router, prefix="/tracks", dependencies=[Depends(get_current_username)]
)
