from uuid import UUID

from pydantic import BaseModel


class TrackBase(BaseModel):
    id: UUID
    name: str
    track_number: int | None = None


class TrackCreate(TrackBase):
    artist_ids: list[UUID] = []
    album_id: UUID | None = None


class SimpleTrack(TrackBase):
    class Config:
        orm_mode = True


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: UUID
    tracks: list[SimpleTrack] = []

    class Config:
        orm_mode = True


class AlbumBase(BaseModel):
    name: str


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: UUID
    tracks: list[SimpleTrack] = []

    class Config:
        orm_mode = True


class Track(TrackBase):
    artists: list[Artist] = []
    album: Album | None = None

    class Config:
        orm_mode = True
