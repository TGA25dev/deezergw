from datetime import datetime
from typing import Any, Dict, Optional
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.exceptions import UnknownException
from deezergw.resources.track import Track


class Playlist:
    def __init__(
        self,
        playlist_metadata: Any,
        api: DeezerAPI,
        favorite_tracks: Dict[str, datetime],
        is_favorite: Optional[bool] = None,
    ) -> None:
        self._api = api
        data = playlist_metadata["DATA"]

        self.id: str = data["PLAYLIST_ID"]
        self.name: str = data["TITLE"]
        self.is_favorite: Optional[bool] = None
        if is_favorite is not None:
            self.is_favorite = is_favorite
        elif "IS_FAVORITE" in data:
            self.is_favorite = data["IS_FAVORITE"]

        self.author_name: str = data["PARENT_USERNAME"]
        self.author_id: str = data["PARENT_USER_ID"]

        self.description: Optional[str] = (
            data["DESCRIPTION"] if "DESCRIPTION" in data else None
        )
        self.duration: Optional[int] = (
            int(data["DURATION"]) if "DURATION" in data else None
        )

        self.last_edited: Optional[datetime] = (
            datetime.fromisoformat(data["DATA_MOD"]) if "DATA_MOD" in data else None
        )

        self._author_pic: Optional[str] = (
            data["PARENT_USER_PICTURE"] if "PARENT_USER_PICTURE" in data else None
        )
        self._playlist_pic: str = data["PLAYLIST_PICTURE"]

        self.songs = (
            tuple(
                Track(metadata, api, favorite_tracks)
                for metadata in playlist_metadata["SONGS"]["data"]
            )
            if "SONGS" in playlist_metadata
            else None
        )

    def favorite(self, forced_value: Optional[bool] = None):
        if forced_value is None:
            if self.is_favorite is None:
                raise UnknownException(
                    "IsFavorite is unknown as the Playlist wasn't directly initialized. You need to specify forced_value in this case."
                )
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value == True:
            self._api.add_favorite_playlist(self.id)
        else:
            self._api.remove_favorite_playlist(self.id)
        self.is_favorite = forced_value
        return self.is_favorite

    def cover_url(self, size: str | int) -> str:
        return IMAGE_URL.format("playlist", self._playlist_pic, size, size)

    def author_picture_url(self, size: str | int) -> str | None:
        if not self._author_pic:
            return
        return IMAGE_URL.format("user", self._author_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - Playlist: "{self.name}" by "{self.author_name}">'
