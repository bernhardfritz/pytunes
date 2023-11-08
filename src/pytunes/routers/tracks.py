from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/{track_id}.m3u8")
async def get_track_playlist(track_id: UUID):
    return FileResponse(f"/data/.pytunes/{track_id}.m3u8")


@router.get("/{track_id}.{segment_index}.m4a")
async def get_track_segment(track_id: UUID, segment_index: int):
    return FileResponse(f"/data/.pytunes/{track_id}.{segment_index}.m4a")
