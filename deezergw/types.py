from typing import List, Literal, TypeVar, TypedDict, Tuple, Set
from deezergw.globals import FormatType, QualityType


class MediaCipherType(TypedDict):
    type: Literal["BF_CBC_STRIPE"]


class MediaSource(TypedDict):
    url: str
    provider: str


class MediaData(TypedDict):
    media_type: Literal["FULL"]
    cipher: MediaCipherType
    format: QualityType
    sources: List[MediaSource]
    media_version: int
    filesize: int
    nbf: int
    exp: int


# -


class LoginDumpData(TypedDict):
    lang: str
    license_token: str
    api_token: str
    jwt: str
    user_id: str


class DownloadInfo(TypedDict):
    quality: QualityType
    file_format: FormatType
    track_id: str


_array = TypeVar("_array")
ArrayLike = List[_array] | Tuple[_array, ...] | Set[_array]
