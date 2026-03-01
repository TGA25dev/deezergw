from typing import Any, Dict, Optional
from datetime import datetime
from deezergw.exceptions import ExpiredException
from deezergw.globals import Qualities, QualityType, StockQuality
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.types import DownloadInfo


def _get_filesizes(track_metadata: Any):
    all_size_keys = list(filter(lambda x: x.startswith("FILESIZE_"), track_metadata))

    sizes: Dict[str, int] = {}

    for key in all_size_keys:
        size: str = key.split("_", 1)[1]
        value: int = int(track_metadata[key])
        if value == 0:
            continue
        sizes[size] = value
    return sizes


class Track:
    def __init__(
        self, track_metadata: Any, api: DeezerAPI, favorite_tracks: Dict[str, datetime]
    ) -> None:
        self._api = api  # Pass through for downloads

        self.id: str = track_metadata["SNG_ID"]
        self.title: str = track_metadata["SNG_TITLE"]
        self.is_favorite = self.id in favorite_tracks

        self.album_name: str = track_metadata["ALB_TITLE"]
        self.album_id: str = track_metadata["ALB_ID"]

        self.artist_name: str = track_metadata["ART_NAME"]
        self.artist_id: str = track_metadata["ART_ID"]

        self.duration: int = int(track_metadata["DURATION"])
        self.release_date: Optional[datetime] = (
            datetime.fromisoformat(track_metadata["DIGITAL_RELEASE_DATE"])
            if "DIGITAL_RELEASE_DATE" in track_metadata
            else None
        )

        self._album_cover_pic: str = track_metadata["ALB_PICTURE"]

        # Maybe add FALLBACK support here later, let's just see if it's required anymore
        self._track_token: str = track_metadata["TRACK_TOKEN"]
        self._track_token_expiary_date = datetime.fromtimestamp(
            track_metadata["TRACK_TOKEN_EXPIRE"]
        )
        self._filesizes = _get_filesizes(track_metadata)
        self._default_filesize = int(track_metadata["FILESIZE"])

    def favorite(self, forced_value: Optional[bool] = None):
        """Toggles is_favorite. Is forced_value specified it will be forced to that value"""
        if forced_value is None:
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value == True:
            self._api.add_favorite_tracks((self.id,))
        else:
            self._api.remove_favorite_tracks((self.id,))
        self.is_favorite = forced_value
        return self.is_favorite

    def cover_url(self, size: str | int) -> str:
        return IMAGE_URL.format("cover", self._album_cover_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - Track: "{self.title}" by "{self.artist_name}" ({self.album_name})>'

    def download_encrypted(
        self, quality: QualityType = StockQuality
    ) -> tuple[bytes, DownloadInfo]:
        now = datetime.now()
        if now > self._track_token_expiary_date:
            raise ExpiredException(
                "Track Token has expired. Please refresh the Track object"
            )

        if quality not in self._filesizes:
            print("Selected quality is not avaliable!")
            for key, value in self._filesizes.items():
                if value == self._default_filesize:
                    print(f"Selected {key} as fallback.")
                    quality = key  # pyright: ignore[reportAssignmentType]
                    break

        media_data = self._api.get_media_data(self._track_token, quality)
        song_link = media_data["sources"][0]["url"]

        crypted_audio = self._api.session.get(song_link)
        if len(crypted_audio.content) == 0:
            raise Exception("CryptedAudio is empty")

        sel_quality = Qualities[quality]

        info: DownloadInfo = {
            "file_format": sel_quality["f_format"],
            "quality": quality,
            "track_id": self.id,
        }

        return crypted_audio.content, info
