from typing import Any, Callable, Optional, Union
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.resources.artist import Artist


class SearchArtist:
    def __init__(
        self,
        artist_metadata: Any,
        api: DeezerAPI,
        get_full_artist: Callable[[str], Artist],
    ) -> None:
        self._api = api

        self.id: str = artist_metadata["id"]
        self.name: str = artist_metadata["name"]

        self.is_favorite: bool = artist_metadata["isFavorite"]
        self.fans: int = artist_metadata["fansCount"]

        self._artist_cover_pic: str = artist_metadata["picture"]["id"]
        self._get_full_artist = get_full_artist

    def get_full_artist(self):
        return self._get_full_artist(self.id)

    def cover_url(self, size: Union[str, int]) -> str:
        return IMAGE_URL.format("artist", self._artist_cover_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - SearchArtist: "{self.name}">'

    def favorite(self, forced_value: Optional[bool] = None):
        if forced_value is None:
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value == True:
            self._api.add_favorite_artist(self.id)
        else:
            self._api.remove_favorite_artist(self.id)
        self.is_favorite = forced_value
        return self.is_favorite
