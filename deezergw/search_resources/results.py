from typing import List
from deezergw.search_resources.album import SearchAlbum
from deezergw.search_resources.artist import SearchArtist
from deezergw.search_resources.playlist import SearchPlaylist
from deezergw.search_resources.track import SearchTrack


class SearchResults:
    def __init__(
        self,
        query: str,
        albums: List[SearchAlbum],
        tracks: List[SearchTrack],
        artists: List[SearchArtist],
        playlists: List[SearchPlaylist],
    ) -> None:
        self.query = query
        self.albums = albums
        self.tracks = tracks
        self.artists = artists
        self.playlists = playlists

    def __repr__(self) -> str:
        return f'<Deezer - SearchResults for "{self.query}": {len(self.albums)} Albums, {len(self.tracks)} Tracks, {len(self.artists)} Artists and {len(self.playlists)} Playlists>'
