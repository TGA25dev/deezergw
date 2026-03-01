from datetime import datetime
from typing import Any, Callable, Dict, Optional
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.resources.track import Track


class SearchTrack:
    def __init__(
        self,
        track_metadata: Any,
        api: DeezerAPI,
        get_full_track: Callable[[str], Track],
        favorite_tracks: Dict[str, datetime],
    ) -> None:
        self._api = api

        self.id: str = track_metadata["id"]
        self.title: str = track_metadata["title"]

        self.is_favorite = self.id in favorite_tracks
        self.duration: int = track_metadata["duration"]

        self.album_id: str = track_metadata["album"]["id"]
        self.album_name: str = track_metadata["album"]["displayTitle"]

        self.artist_name: str = track_metadata["contributors"]["edges"][0]["node"][
            "name"
        ]
        self.artist_id: str = track_metadata["contributors"]["edges"][0]["node"]["id"]

        self._album_cover_pic: str = track_metadata["album"]["cover"]["id"]
        self._get_full_track = get_full_track

    def get_full_track(self):
        return self._get_full_track(self.id)

    def cover_url(self, size: str | int) -> str:
        return IMAGE_URL.format("cover", self._album_cover_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - SearchTrack: "{self.title}" by "{self.artist_name}" ({self.album_name})>'

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
