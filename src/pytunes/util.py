import glob
import hashlib
import os
import subprocess
from uuid import UUID

import eyed3
from fastapi import Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .dependencies import get_db


def mp3_to_hls(track_file_path: str, track_id: UUID):
    p = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            f"{track_file_path}",
            "-vn",
            "-ac",
            "2",
            "-acodec",
            "aac",
            "-muxdelay",
            "0",
            "-f",
            "segment",
            "-segment_format",
            "mpegts",
            "-segment_time",
            "6",
            "-segment_list",
            f"/data/.pytunes/{track_id}.m3u8",
            f"/data/.pytunes/{track_id}.%d.m4a",
        ]
    )
    return p.returncode


def create_track_internal(db: Session, file_path: str, id: UUID):
    if mp3_to_hls(file_path, id):
        return
    db_track = crud.create_track(
        db, schemas.TrackCreate(id=id, name=os.path.basename(file_path))
    )
    try:
        id3 = eyed3.load(file_path)
        if id3:
            album_name, artist, title, track_num = (
                id3.tag.album,
                id3.tag.artist,
                id3.tag.title,
                id3.tag.track_num,
            )
            if album_name:
                db_album = crud.get_album_by_name(db, album_name) or crud.create_album(
                    db, schemas.AlbumCreate(name=album_name)
                )
                db_track.album = db_album
            if artist:
                artist_names = [
                    artist_name.strip() for artist_name in artist.split(";")
                ]
                for artist_name in artist_names:
                    db_artist = crud.get_artist_by_name(
                        db, artist_name
                    ) or crud.create_artist(db, schemas.ArtistCreate(name=artist_name))
                    db_track.artists.append(db_artist)
            if title:
                db_track.name = title
            if track_num:
                (track_number, total_number_of_tracks) = track_num
                if track_number:
                    db_track.track_number = track_number
    except IOError as err:
        print(err)
    except BaseException:
        pass
    db.commit()


def create_track(file_path: str, id: UUID):
    db = next(get_db(), None)
    create_track_internal(db, file_path, id)


def sha1_to_uuid(sha1: str):
    return UUID(sha1[:32])


def sha1sum(file_path: str):
    with open(file_path, "rb") as f:
        digest = hashlib.file_digest(f, "sha1")
    return digest.hexdigest()


def handle_created(file_path: str):
    db = next(get_db(), None)
    id = sha1_to_uuid(sha1sum(file_path))
    create_track_internal(db, file_path, id)


def delete_track(db: Session, id: UUID):
    for file_path in glob.glob(f"/data/.pytunes/{id}.*"):
        os.remove(file_path)
    crud.delete_track(db, id)


def cleanup(db: Session):
    db_ids = crud.get_track_ids(db)
    fs_ids = {}
    for file_path in glob.glob("/data/**/*.mp3", recursive=True):
        fs_ids[sha1_to_uuid(sha1sum(file_path))] = file_path
    removed = [id for id in db_ids if id not in fs_ids]
    for id in removed:
        delete_track(db, id)


def handle_deleted():
    db = next(get_db(), None)
    cleanup(db)


def artist_to_playlist_item(request: Request, artist: models.Artist) -> str:
    return "\n".join(
        [
            f"#EXTINF:-1,{artist.name}",
            request.url_for("get_artist_playlist", artist_id=artist.id)._url,
        ]
    )


def album_to_playlist_item(request: Request, album: models.Album) -> str:
    return "\n".join(
        [
            f"#EXTINF:-1,{album.name}",
            request.url_for("get_album_playlist", album_id=album.id)._url,
        ]
    )


def track_to_playlist_item(request: Request, track: models.Track) -> str:
    colonSeparatedArtists = ", ".join(map(lambda artist: artist.name, track.artists))
    return "\n".join(
        [
            f"#EXTINF:-1,{colonSeparatedArtists}{' - ' if track.artists else ''}{track.name}",
            request.url_for("get_track_playlist", track_id=track.id)._url,
        ]
    )


def has_tracks(artistOrAlbum: models.Artist | models.Album) -> bool:
    return bool(artistOrAlbum.tracks)
