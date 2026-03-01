import json as _json
from os import PathLike
from typing import Any, Generator, List, Optional, Union
from deezergw.api import DeezerAPI
from deezergw import decrypt_utils as _decrypt_utils
from deezergw.resources.album import Album
from deezergw.resources.artist import Artist
from deezergw.resources.playlist import Playlist
from deezergw.resources.track import Track
from deezergw.search_resources.album import SearchAlbum
from deezergw.search_resources.artist import SearchArtist
from deezergw.search_resources.playlist import SearchPlaylist
from deezergw.search_resources.results import SearchResults
from deezergw.search_resources.track import SearchTrack
from deezergw.types import ArrayLike, LoginDumpData


class Client:
    def __init__(
        self,
        key: str,
        arl: Optional[str] = None,
        logindump: Optional[bytes] = None,
    ) -> None:
        """Creates a new Client. Log in by either specifying an arl or an existing logindump"""
        self._key = key

        if arl:
            self._api = DeezerAPI(arl)
        elif logindump:
            data = _decrypt_utils.decrypt(logindump, key)
            arl, main = data.split("|$|", 1)

            main_data: LoginDumpData = _json.loads(main)
            self._api = DeezerAPI(arl, main_data)
        else:
            raise Exception("No secret specified")
        self.favorited_ids = self._api.favorited_ids

        self.add_favorite_album = self._api.add_favorite_album
        self.add_favorite_artist = self._api.add_favorite_artist
        self.add_favorite_playlist = self._api.add_favorite_playlist
        self.add_favorite_tracks = self._api.add_favorite_tracks

        self.remove_favorite_album = self._api.remove_favorite_album
        self.remove_favorite_artist = self._api.remove_favorite_artist
        self.remove_favorite_playlist = self._api.remove_favorite_playlist
        self.remove_favorite_tracks = self._api.remove_favorite_tracks

    def generate_logindump(self):
        """
        Generates a encrypted byte string that can be used to log into your account with DeezerGW.
        Please note that this is NOT fully uncrackable as Python will always be easy to "decompile".
        It's purpose is to be harder to find or crack by any potential malware or analysts and provide a quicker login time.
        """
        if not self._api.lang:
            raise Exception("Lang was not obtained")
        if not self._api.user_id:
            raise Exception("UserID was not obtained")
        if not self._api._license_expire or not self._api._license_token:
            raise Exception("License Token was not obtained")

        main_data: LoginDumpData = {
            "api_token": self._api._api_token,
            "jwt": self._api._jwt,
            "lang": self._api.lang,
            "license_token": self._api._license_token,
            "user_id": self._api.user_id,
        }
        main = _json.dumps(main_data)

        data = self._api._arl + "|$|" + main
        return _decrypt_utils.encrypt(data, self._key)

    # Single functions

    def get_track(self, id: Union[str, int]):
        metadata = self._api.get_track_data(id)
        return Track(metadata, self._api, self.favorited_ids)

    def get_album(self, id: Union[str, int]):
        is_favorite = self._api.is_album_favorited(id)
        metadata = self._api.get_album_data(id)
        return Album(metadata, self._api, self.favorited_ids, is_favorite)

    def get_artist(self, id: Union[str, int]):
        is_favorite = self._api.is_artist_favorited(id)
        metadata = self._api.get_artist_data(id)
        return Artist(metadata, self._api, self.favorited_ids, is_favorite)

    def get_playlist(self, id: Union[str, int], start_offset: int = 0):
        metadata = self._api.get_playlist_data(id, start_offset)
        return Playlist(metadata, self._api, self.favorited_ids)

    def search(self, query: str):
        response = self._api.search(query)
        results = response["instantSearch"]["results"]

        return_data = SearchResults(query, [], [], [], [])

        for album_metadata in results["albums"]["edges"]:
            album = SearchAlbum(
                album_metadata["node"], self._api, self.get_album
            )
            return_data.albums.append(album)

        for track_metadata in results["tracks"]["edges"]:
            track = SearchTrack(
                track_metadata["node"],
                self._api,
                self.get_track,
                self.favorited_ids,
            )
            return_data.tracks.append(track)

        for artist_metadata in results["artists"]["edges"]:
            artist = SearchArtist(
                artist_metadata["node"], self._api, self.get_artist
            )
            return_data.artists.append(artist)

        for playlist_metadata in results["playlists"]["edges"]:
            playlist = SearchPlaylist(
                playlist_metadata["node"], self._api, self.get_playlist
            )
            return_data.playlists.append(playlist)

        return return_data

    # Batch functions

    def get_tracks(self, ids: ArrayLike[str]):
        metadatas = self._api.get_track_batch_data(ids)
        tracks: List[Track] = []
        for metadata in metadatas["data"]:
            tracks.append(Track(metadata, self._api, self.favorited_ids))
        return tracks

    # Favorite Functions

    def get_favorite_tracks(self):
        return self.get_tracks(tuple(self.favorited_ids.keys()))

    def get_favorite_albums(self):
        if not self._api.user_id:
            raise Exception("UserID was not obtained")
        metadatas = self._api.get_profile_page_tab("albums", self._api.user_id)
        albums: List[Album] = []
        for metadata in metadatas["TAB"]["albums"]["data"]:
            albums.append(
                Album({"DATA": metadata}, self._api, self.favorited_ids, True)
            )
        return albums

    def get_favorite_artists(self):
        if not self._api.user_id:
            raise Exception("UserID was not obtained")
        metadatas = self._api.get_profile_page_tab(
            "artists", self._api.user_id
        )
        artists: List[Artist] = []
        for metadata in metadatas["TAB"]["artists"]["data"]:
            artists.append(
                Artist({"DATA": metadata}, self._api, self.favorited_ids, True)
            )
        return artists

    def get_favorite_playlists(self):
        if not self._api.user_id:
            raise Exception("UserID was not obtained")
        metadatas = self._api.get_profile_page_tab(
            "playlists", self._api.user_id
        )
        playlists: List[Playlist] = []
        for metadata in metadatas["TAB"]["playlists"]["data"]:
            playlists.append(
                Playlist(
                    {"DATA": metadata}, self._api, self.favorited_ids, True
                )
            )
        return playlists


def decrypt_audio(crypted_audio: bytes, track_id: Union[str, int]):
    decrypt_key = _decrypt_utils.calc_bf_key(str(track_id))

    for seg, data in enumerate(_decrypt_utils.iter_bytes(crypted_audio, 2048)):
        if seg % 3 == 0 and len(data) == 2048:
            data = _decrypt_utils.blowfish_decrypt(data, decrypt_key)

        yield data


def save_decrypted(
    decrypted_audio: Generator[bytes, Any, None], path: Union[PathLike, str]
):
    with open(path, "wb") as f:
        f.writelines(decrypted_audio)
