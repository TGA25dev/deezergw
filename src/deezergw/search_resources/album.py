from datetime import datetime
from typing import Any, Callable, Optional, Union
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.resources.album import Album


class SearchAlbum:
    def __init__(
        self,
        album_metadata: Any,
        api: DeezerAPI,
        get_full_album: Callable[[str], Album],
    ) -> None:
        self._api = api

        self.id: str = album_metadata["id"]
        self.name: str = album_metadata["displayTitle"]

        self.artist_name: str = album_metadata["contributors"]["edges"][0][
            "node"
        ]["name"]
        self.artist_id: str = album_metadata["contributors"]["edges"][0][
            "node"
        ]["id"]

        self.is_favorite: bool = album_metadata["isFavorite"]
        self.release_date: datetime = datetime.fromisoformat(
            album_metadata["releaseDateAlbum"]
        )

        self._album_cover_pic: str = album_metadata["cover"]["id"]
        self._get_full_album = get_full_album

    def get_full_album(self):
        """
        Get all missing data for this album

        :return: A full Album instance
        :rtype: Album
        """
        return self._get_full_album(self.id)

    def cover_url(self, size: Union[str, int]) -> str:
        return IMAGE_URL.format("cover", self._album_cover_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - SearchAlbum: "{self.name}" by "{self.artist_name}">'

    def favorite(self, forced_value: Optional[bool] = None):
        if forced_value is None:
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value is True:
            self._api.add_favorite_album(self.id)
        else:
            self._api.remove_favorite_album(self.id)
        self.is_favorite = forced_value
        return self.is_favorite
