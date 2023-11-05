import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base

artists_tracks = Table(
    "artists_tracks",
    Base.metadata,
    Column("artist_id", ForeignKey("artists.id"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
)


class Track(Base):
    __tablename__ = "tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, index=True)
    album_id = Column(UUID(as_uuid=True), ForeignKey("albums.id"))
    track_number = Column(Integer, index=True)

    artists = relationship("Artist", secondary=artists_tracks, back_populates="tracks")
    album = relationship("Album", back_populates="tracks")


class Album(Base):
    __tablename__ = "albums"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)

    tracks = relationship("Track", order_by=Track.track_number, back_populates="album")


class Artist(Base):
    __tablename__ = "artists"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)

    tracks = relationship(
        "Track", secondary=artists_tracks, order_by=Track.name, back_populates="artists"
    )
