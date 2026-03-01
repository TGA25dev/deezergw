from typing import Any, Callable, Optional, Union
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.resources.playlist import Playlist


class SearchPlaylist:
    def __init__(
        self,
        playlist_metadata: Any,
        api: DeezerAPI,
        get_full_playlist: Callable[[str], Playlist],
    ) -> None:
        self._api = api

        self.id: str = playlist_metadata["id"]
        self.name: str = playlist_metadata["title"]

        self.author_name: Optional[str] = None
        self.author_id: Optional[str] = None
        if "owner" in playlist_metadata and playlist_metadata["owner"]:
            self.author_name = playlist_metadata["owner"]["name"]
            self.author_id = playlist_metadata["owner"]["id"]

        self.is_favorite: bool = playlist_metadata["isFavorite"]
        self.fans: int = playlist_metadata["fansCount"]

        self._playlist_pic: str = playlist_metadata["picture"]["id"]
        self._get_full_playlist = get_full_playlist

    def get_full_playlist(self):
        return self._get_full_playlist(self.id)

    def cover_url(self, size: Union[str, int]) -> str:
        return IMAGE_URL.format("playlist", self._playlist_pic, size, size)

    def __repr__(self) -> str:
        return (
            f'<Deezer - SearchPlaylist: "{self.name}" by "{self.author_name}">'
        )

    def favorite(self, forced_value: Optional[bool] = None):
        if forced_value is None:
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value is True:
            self._api.add_favorite_playlist(self.id)
        else:
            self._api.remove_favorite_playlist(self.id)
        self.is_favorite = forced_value
        return self.is_favorite
