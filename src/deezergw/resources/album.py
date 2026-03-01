from datetime import datetime
from typing import Any, Dict, Optional, Union
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.exceptions import UnknownException
from deezergw.resources.track import Track


class Album:
    def __init__(
        self,
        album_metadata: Any,
        api: DeezerAPI,
        favorite_tracks: Dict[str, datetime],
        is_favorite: Optional[bool] = None,
    ) -> None:
        self._api = api
        data = album_metadata["DATA"]

        self.id: str = data["ALB_ID"]
        self.name: str = data["ALB_TITLE"]

        self.artist_name: str = data["ART_NAME"]
        self.artist_id: str = (
            data if "ART_ID" in data else data["ARTISTS"][0]
        )["ART_ID"]

        self.duration: Optional[int] = (
            int(data["DURATION"]) if "DURATION" in data else None
        )

        self.fans: Optional[int] = (
            int(data["NB_FAN"]) if "NB_FAN" in data else None
        )
        self.is_favorite = is_favorite

        self.release_date: Optional[datetime] = None
        if "DIGITAL_RELEASE_DATE" in data:
            self.release_date = datetime.fromisoformat(
                data["DIGITAL_RELEASE_DATE"]
            )
        elif "PHYSICAL_RELEASE_DATE" in data:
            self.release_date = datetime.fromisoformat(
                data["PHYSICAL_RELEASE_DATE"]
            )

        self._album_cover_pic: str = data["ALB_PICTURE"]

        self.tracks = (
            tuple(
                Track(metadata, api, favorite_tracks)
                for metadata in album_metadata["SONGS"]["data"]
            )
            if "SONGS" in album_metadata
            else None
        )

    def favorite(self, forced_value: Optional[bool] = None):
        if forced_value is None:
            if self.is_favorite is None:
                raise UnknownException(
                    "IsFavorite is unknown as the Album wasn't directly initialized. You need to specify forced_value in this case."
                )
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value is True:
            self._api.add_favorite_album(self.id)
        else:
            self._api.remove_favorite_album(self.id)
        self.is_favorite = forced_value
        return self.is_favorite

    def cover_url(self, size: Union[str, int]) -> str:
        return IMAGE_URL.format("cover", self._album_cover_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - Album: "{self.name}" by "{self.artist_name}">'
