from uuid import UUID
from pytunes.util import sha1_to_uuid


def test_sha1_to_uuid():
    assert sha1_to_uuid("0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33") == UUID(
        "0beec7b5-ea3f-0fdb-c95d-0dd47f3c5bc2"
    )
