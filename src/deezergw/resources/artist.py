from datetime import datetime
from typing import Any, Dict, Optional, Union
from deezergw.api import IMAGE_URL, DeezerAPI
from deezergw.exceptions import UnknownException
from deezergw.resources.album import Album
from deezergw.resources.playlist import Playlist
from deezergw.resources.track import Track


class Artist:
    def __init__(
        self,
        artist_metadata: Any,
        api: DeezerAPI,
        favorite_tracks: Dict[str, datetime],
        is_favorite: Optional[bool] = None,
    ) -> None:
        self._api = api
        data = artist_metadata["DATA"]

        self.id: str = data["ART_ID"]
        self.name: str = data["ART_NAME"]

        self.is_favorite = is_favorite
        self.fans: int = int(data["NB_FAN"])
        self.bio: Optional[str] = None
        if "BIO" in artist_metadata and artist_metadata["BIO"] != False:
            self.bio = tuple(artist_metadata["BIO"].values())[0]

        self.highlight_album: Optional[Album] = None

        if (
            "HIGHLIGHT" in artist_metadata
            and artist_metadata["HIGHLIGHT"]["TYPE"] == "album"
        ):
            highlight_data = {
                "DATA": artist_metadata["HIGHLIGHT"]["ITEM"],
                "SONGS": artist_metadata["HIGHLIGHT"]["ITEM"]["SONGS"],
            }
            self.highlight_album = Album(highlight_data, api, favorite_tracks)

        self.top_tracks = (
            tuple(
                Track(metadata, api, favorite_tracks)
                for metadata in artist_metadata["TOP"]["data"]
            )
            if "TOP" in artist_metadata
            else None
        )
        self.related_artists = (
            tuple(
                Artist({"DATA": metadata}, api, favorite_tracks)
                for metadata in artist_metadata["RELATED_ARTISTS"]["data"]
            )
            if "RELATED_ARTISTS" in artist_metadata
            else None
        )
        self.related_playlists = (
            tuple(
                Playlist({"DATA": metadata}, api, favorite_tracks)
                for metadata in artist_metadata["RELATED_PLAYLIST"]["data"]
            )
            if "RELATED_PLAYLIST" in artist_metadata
            else None
        )
        self.albums = (
            tuple(
                Album({"DATA": metadata}, api, favorite_tracks)
                for metadata in artist_metadata["ALBUMS"]["data"]
            )
            if "ALBUMS" in artist_metadata
            else None
        )

        self._artist_cover_pic: str = data["ART_PICTURE"]

    def favorite(self, forced_value: Optional[bool] = None):
        if forced_value is None:
            if self.is_favorite is None:
                raise UnknownException(
                    "IsFavorite is unknown as the Artist wasn't directly initialized. You need to specify forced_value in this case."
                )
            forced_value = not self.is_favorite

        if forced_value == self.is_favorite:
            return forced_value

        if forced_value is True:
            self._api.add_favorite_artist(self.id)
        else:
            self._api.remove_favorite_artist(self.id)
        self.is_favorite = forced_value
        return self.is_favorite

    def cover_url(self, size: Union[str, int]) -> str:
        return IMAGE_URL.format("artist", self._artist_cover_pic, size, size)

    def __repr__(self) -> str:
        return f'<Deezer - Artist: "{self.name}">'
