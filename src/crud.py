from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from . import models, schemas


def create_artist(db: Session, artist: schemas.ArtistCreate) -> models.Artist:
    db_artist = models.Artist(name=artist.name)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


def get_artist_by_name(db: Session, artist_name: str) -> models.Artist | None:
    db_artist = (
        db.query(models.Artist).filter(models.Artist.name == artist_name).first()
    )
    return db_artist


def get_artists(db: Session) -> list[models.Artist]:
    return db.query(models.Artist).order_by(models.Artist.name).all()


def get_artist_albums(db: Session, artist_id: UUID) -> list[models.Album]:
    return (
        db.execute(
            select(models.Album)
            .join(models.Track, models.Album.id == models.Track.album_id)
            .join(
                models.artists_tracks,
                models.Track.id == models.artists_tracks.c.track_id,
            )
            .where(models.artists_tracks.c.artist_id == artist_id)
            .order_by(models.Album.name)
        )
        .scalars()
        .unique()
    )


def create_album(db: Session, album: schemas.AlbumCreate) -> models.Album:
    db_album = models.Album(name=album.name)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def get_album_by_name(db: Session, album_name: str) -> models.Album | None:
    return db.query(models.Album).filter(models.Album.name == album_name).first()


def create_track(db: Session, track: schemas.TrackCreate) -> models.Track:
    db_track = models.Track(id=track.id, name=track.name)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def get_track_ids(db: Session) -> list[UUID]:
    return [id for (id,) in db.query(models.Track.id).all()]


def delete_track(db: Session, track_id: UUID):
    db_track: models.Track | None = db.query(models.Track).get(track_id)
    if not db_track:
        return
    db.delete(db_track)
    db.commit()


def get_artist_tracks_without_album(db: Session, artist_id: UUID) -> list[models.Track]:
    return (
        db.execute(
            select(models.Track)
            .join(
                models.artists_tracks,
                models.Track.id == models.artists_tracks.c.track_id,
            )
            .where(
                and_(
                    models.artists_tracks.c.artist_id == artist_id,
                    models.Track.album_id == None, # noqa: E711
                )
            )
            .order_by(models.Track.name)
        )
        .scalars()
        .unique()
    )


def get_album_tracks(db: Session, album_id: UUID) -> list[models.Track]:
    return (
        db.query(models.Track)
        .filter(models.Track.album_id == album_id)
        .order_by(models.Track.track_number)
        .all()
    )


def get_tracks_without_artists(db: Session) -> list[models.Track]:
    return (
        db.query(models.Track)
        .filter(
            models.Track.id.not_in(
                db.query(models.artists_tracks.c.track_id).distinct()
            )
        )
        .order_by(models.Track.name)
        .all()
    )
