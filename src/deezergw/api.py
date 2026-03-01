from datetime import datetime
from requests import Session
from typing import Any, Dict, Optional, Tuple, Union
from deezergw.exceptions import NoRightOnMedia
from deezergw.globals import Qualities, QualityType
from deezergw.types import ArrayLike, LoginDumpData, MediaData

METHOD_GET_USER_DATA = "deezer.getUserData"
METHOD_GET_USER_PROFILE = "deezer.pageProfile"

METHOD_GET_ALBUM_DATA = "deezer.pageAlbum"

METHOD_GET_TRACK_DATA = "song.getData"
METHOD_GET_BATCH_TRACK_DATA = "song.getListData"
METHOD_GET_FAVORITE_TRACKS = "song.getFavoriteIds"
METHOD_ADD_FAVORITE_TRACKS = "song.addFavorites"
METHOD_REMOVE_FAVORITE_TRACKS = "song.removeFavorites"

METHOD_GET_ARTIST_DATA = "deezer.pageArtist"
METHOD_ADD_FAVORITE_ARTIST = "artist.addFavorite"
METHOD_REMOVE_FAVORITE_ARTIST = "artist.deleteFavorite"

METHOD_GET_PLAYLIST_DATA = "deezer.pagePlaylist"
METHOD_ADD_FAVORITE_PLAYLIST = "playlist.addFavorite"
METHOD_REMOVE_FAVORITE_PLAYLIST = "playlist.deleteFavorite"

PRIVATE_API_URL = "https://www.deezer.com/ajax/gw-light.php"
GET_MEDIA_URL = "https://media.deezer.com/v1/get_url"
GET_JWT_ARL_URL = "https://auth.deezer.com/login/arl?jo=p&rto=c&i=c"
GRAPHQL_URL = "https://pipe.deezer.com/api"
IMAGE_URL = "https://cdn-images.dzcdn.net/images/{}/{}/{}x{}-000000-80-0-0.jpg"

GRAPHQL_IS_ARTIST_FAVORITE = (
    "IsArtistFavorite",
    "query IsArtistFavorite($artistId: String!) { artist(artistId: $artistId) { isFavorite } }",
)
GRAPHQL_IS_ALBUM_FAVORITE = (
    "IsAlbumFavorite",
    "query IsAlbumFavorite($albumId: String!) { album(albumId: $albumId) { isFavorite } }",
)
GRAPHQL_ADD_ALBUM_FAVORITE = (
    "AddAlbumToFavorite",
    "mutation AddAlbumToFavorite($albumId: String!) { addAlbumToFavorite(albumId: $albumId) { album { id isFavorite } } }",
)
GRAPHQL_REMOVE_ALBUM_FAVORITE = (
    "RemoveAlbumFromFavorite",
    "mutation RemoveAlbumFromFavorite($albumId: String!) { removeAlbumFromFavorite(albumId: $albumId) { album { id isFavorite } } }",
)
GRAPHQL_SEARCH = (
    "SearchFull",
    "query SearchFull($query: String!, $firstGrid: Int!, $firstList: Int!, $includeRelatedContent: Boolean!, $channelPlaylistFirst: Int!) { instantSearch(query: $query) { bestResult { __typename ... on InstantSearchAlbumBestResult { album { ...SearchAlbum __typename } __typename } ... on InstantSearchArtistBestResult { artist { ...BestResultArtist __typename } relatedContent @include(if: $includeRelatedContent) { ...RelatedContentArtist __typename } __typename } ... on InstantSearchPlaylistBestResult { playlist { ...SearchPlaylist __typename } __typename } ... on InstantSearchPodcastBestResult { podcast { ...SearchPodcast __typename } __typename } ... on InstantSearchLivestreamBestResult { livestream { ...SearchLivestream __typename } __typename } ... on InstantSearchTrackBestResult { foundByLyrics track { ...TableTrack __typename } __typename } ... on InstantSearchPodcastEpisodeBestResult { podcastEpisode { ...SearchPodcastEpisode __typename } __typename } ... on InstantSearchFlowConfigBestResult { flowConfig { ...SearchFlowConfig __typename } __typename } ... on InstantSearchChannelBestResult { channel { ...SearchChannel __typename } relatedContent { ...ChannelBestResultRelatedContent __typename } __typename } } results { artists(first: $firstGrid) { edges { node { ...SearchArtist __typename } __typename } pageInfo { endCursor __typename } priority __typename } albums(first: $firstGrid) { edges { node { ...SearchAlbum __typename } __typename } pageInfo { endCursor __typename } priority __typename } channels(first: $firstGrid) { edges { node { ...SearchChannel __typename } __typename } pageInfo { endCursor __typename } priority __typename } flowConfigs(first: $firstGrid) { edges { node { ...SearchFlowConfig __typename } __typename } pageInfo { endCursor __typename } priority __typename } livestreams(first: $firstGrid) { edges { node { ...SearchLivestream __typename } __typename } pageInfo { endCursor __typename } priority __typename } playlists(first: $firstGrid) { edges { node { ...SearchPlaylist __typename } __typename } pageInfo { endCursor __typename } priority __typename } podcasts(first: $firstGrid) { edges { node { ...SearchPodcast __typename } __typename } pageInfo { endCursor __typename } priority __typename } tracks(first: $firstList) { edges { node { ...TableTrack __typename } __typename } pageInfo { endCursor __typename } priority __typename } users(first: $firstGrid) { edges { node { ...SearchUser __typename } __typename } pageInfo { endCursor __typename } priority __typename } podcastEpisodes(first: $firstList) { edges { node { ...SearchPodcastEpisode __typename } __typename } pageInfo { endCursor __typename } priority __typename } __typename } __typename } }  fragment SearchAlbum on Album { id displayTitle isFavorite releaseDateAlbum: releaseDate isExplicitAlbum: isExplicit cover { ...PictureLarge __typename } contributors { edges { roles node { ... on Artist { id name __typename } __typename } __typename } __typename } tracksCount __typename }  fragment PictureLarge on Picture { id large: urls(pictureRequest: {width: 500, height: 500}) explicitStatus __typename }  fragment BestResultArtist on Artist { ...SearchArtist hasSmartRadio hasTopTracks __typename }  fragment SearchArtist on Artist { id isFavorite name fansCount picture { ...PictureLarge __typename } __typename }  fragment RelatedContentArtist on InstantSearchArtistBestResultRelatedContent { __typename ... on InstantSearchArtistBestResultRelatedContentNewRelease { album { ...BestResultAlbumWithTracks __typename } __typename } ... on InstantSearchArtistBestResultRelatedContentRelevantAlbum { album { ...BestResultAlbumWithTracks __typename } __typename } ... on InstantSearchArtistBestResultRelatedContentTopTracks { tracks { ...TableTrack __typename } __typename } }  fragment BestResultAlbumWithTracks on Album { ...SearchAlbum tracks { edges { node { ...TableTrack __typename } __typename } __typename } __typename }  fragment TableTrack on Track { id title duration popularity isExplicit lyrics { id __typename } media { id rights { ads { available availableAfter __typename } sub { available availableAfter __typename } __typename } __typename } album { id displayTitle cover { ...PictureXSmall ...PictureLarge __typename } __typename } contributors { edges { node { ... on Artist { id name __typename } __typename } __typename } __typename } __typename }  fragment PictureXSmall on Picture { id xxx_small: urls(pictureRequest: {width: 40, height: 40}) explicitStatus __typename }  fragment SearchPlaylist on Playlist { id title isFavorite estimatedTracksCount fansCount isPrivate isCollaborative picture { ...PictureLarge __typename } owner { id name __typename } __typename }  fragment SearchPodcast on Podcast { id displayTitle isPodcastFavorite: isFavorite cover { ...PictureLarge __typename } isExplicit rawEpisodes __typename }  fragment SearchLivestream on Livestream { id name cover { ...PictureLarge __typename } __typename }  fragment SearchPodcastEpisode on PodcastEpisode { id title description duration releaseDate media { url __typename } podcast { id displayTitle isExplicit cover { ...PictureSmall ...PictureLarge __typename } rights { ads { available __typename } sub { available __typename } __typename } __typename } __typename }  fragment PictureSmall on Picture { id small: urls(pictureRequest: {height: 100, width: 100}) explicitStatus __typename }  fragment SearchFlowConfig on FlowConfig { id title visuals { dynamicPageIcon { id large: urls(uiAssetRequest: {width: 500, height: 500}) __typename } __typename } __typename }  fragment SearchChannel on Channel { id picture { ...PictureLarge __typename } logoAsset { id large: urls(uiAssetRequest: {width: 500, height: 0}) __typename } name slug url { webUrl __typename } backgroundColor __typename }  fragment ChannelBestResultRelatedContent on InstantSearchChannelBestResultRelatedContent { flowConfig { ...SearchFlowConfig __typename } playlists(first: $channelPlaylistFirst) { edges { node { ...SearchPlaylist __typename } __typename } __typename } __typename }  fragment SearchUser on User { id name picture { ...PictureLarge __typename } __typename }",
)


class DeezerAPI:
    def __init__(
        self,
        arl: str,
        logindump_data: Optional[LoginDumpData] = None,
    ) -> None:
        self.session = Session()
        self.session.headers["Origin"] = "https://www.deezer.com"
        self.session.headers["Referer"] = "https://www.deezer.com"
        self.jwt_session = Session()

        self._arl = arl
        self._api_token: str = "null"
        self._jwt: str = "null"
        self.user_id: Optional[str] = None
        self._license_token: Optional[str] = None
        self._license_expire: Optional[int] = None
        self.lang: Optional[str] = None

        if logindump_data:
            self._api_token = logindump_data["api_token"]
            self._jwt = logindump_data["jwt"]
            self.lang = logindump_data["lang"]
            self.user_id = logindump_data["user_id"]
            self._license_token = logindump_data["license_token"]

            self.session.cookies["arl"] = self._arl
            self.jwt_session.headers["authorization"] = "Bearer " + self._jwt
        else:
            self._refresh_token()
            self._refresh_jwt_token()

        self.favorited_ids = self.get_favorited_track_ids()

    def is_logged_in(self) -> bool:
        data = self.get_user_data()

        return data["USER"]["USER_ID"] != 0

    def check_if_logged_in(self, msg: str = "User not logged in"):
        if not self.is_logged_in():
            raise Exception(msg)

    def _refresh_token(self):
        self.session.cookies.clear_session_cookies()

        if not self.is_logged_in():
            self.session.cookies["arl"] = self._arl
            self.check_if_logged_in("Refreshing token failed. ARL invalid?")

        data = self.get_user_data()
        self.lang = data["SETTING_LANG"].lower()
        self.user_id = data["USER"]["USER_ID"]
        self._license_token = data["USER"]["OPTIONS"]["license_token"]
        self._license_expire = data["USER"]["OPTIONS"]["expiration_timestamp"]
        self._api_token = data["checkForm"]

    def _refresh_jwt_token(self):
        jwt_json = self.session.post(GET_JWT_ARL_URL).json()
        if "jwt" not in jwt_json:
            raise Exception("JWT Refresh failed")

        self._jwt = jwt_json["jwt"]
        self.jwt_session.headers["authorization"] = "Bearer " + self._jwt

    def _get_api(
        self, method: str, json_data: Any = None, retries: int = 3
    ) -> Any:
        params = {
            "api_version": "1.0",
            "api_token": self._api_token,
            "input": "3",
            "method": method,
        }

        response = self.session.post(
            PRIVATE_API_URL, params=params, json=json_data
        )

        if response.status_code != 200:
            raise Exception(
                "GetApi didn't return status 200, but "
                + str(response.status_code)
            )

        results = response.json()["results"]

        if not results:
            if retries <= 0:
                raise Exception("Results are empty")
            print(f"Retrying ({retries} tries left) ...")
            retries -= 1
            self._refresh_token()
            return self._get_api(method, json_data, retries=retries)

        return results

    def _request_graphql(
        self, query_pair: Tuple[str, str], variables: Any
    ) -> Any:
        json = {
            "operationName": query_pair[0],
            "query": query_pair[1],
            "variables": variables,
        }
        response = self.jwt_session.post(
            "https://pipe.deezer.com/api", json=json
        )

        if response.status_code != 200:
            raise Exception(
                "GraphQL request failed. Status " + str(response.status_code)
            )

        response_json = response.json()
        if "errors" in response_json:
            if response_json["errors"][0]["type"] == "JwtTokenExpiredError":
                self._refresh_jwt_token()
                return self._request_graphql(query_pair, variables)
            else:
                raise Exception("GraphQL request failed. Unknown JSON Error")

        return response_json["data"]

    def get_user_data(self):
        data = self._get_api(METHOD_GET_USER_DATA)
        return data

    def get_track_data(self, id: Union[str, int]):
        json_data = {"sng_id": str(id)}
        data = self._get_api(METHOD_GET_TRACK_DATA, json_data)

        return data

    def get_album_data(self, id: Union[str, int]):
        if not self.lang:
            raise Exception("Lang was not found during initialization")

        json_data = {
            "alb_id": str(id),
            "header": True,
            "tab": 0,
            "lang": self.lang,
        }
        data = self._get_api(METHOD_GET_ALBUM_DATA, json_data)

        return data

    def get_artist_data(self, id: Union[str, int]):
        if not self.lang:
            raise Exception("Lang was not found during initialization")

        json_data = {"art_id": str(id), "tab": 0, "lang": self.lang}
        data = self._get_api(METHOD_GET_ARTIST_DATA, json_data)

        return data

    def get_playlist_data(self, id: Union[str, int], start: int = 0):
        if not self.lang:
            raise Exception("Lang was not found during initialization")

        json_data = {
            "header": True,
            "lang": self.lang,
            "nb": 40,
            "playlist_id": str(id),
            "start": start,
            "tab": 0,
        }
        data = self._get_api(METHOD_GET_PLAYLIST_DATA, json_data)

        return data

    def get_track_batch_data(self, ids: ArrayLike[str]):
        json_data = {"sng_ids": tuple(ids)}
        data = self._get_api(METHOD_GET_BATCH_TRACK_DATA, json_data)

        return data

    def get_media_data(
        self, track_token: str, quality: QualityType
    ) -> MediaData:
        if not self._license_token:
            raise Exception("No License Token found")

        # Put requested quality first
        sorted_quality = sorted(Qualities, key=lambda x: x != quality)

        json_data = {
            "license_token": self._license_token,
            "media": [
                {
                    "type": "FULL",
                    "formats": [
                        {"cipher": "BF_CBC_STRIPE", "format": qual}
                        for qual in sorted_quality
                    ],
                }
            ],
            "track_tokens": [track_token],
        }

        response = self.session.post(GET_MEDIA_URL, json=json_data)
        infos = response.json()["data"][0]

        if "errors" in infos:
            raise NoRightOnMedia(infos["errors"][0]["message"])

        return infos["media"][0]

    def is_artist_favorited(self, id: Union[str, int]) -> bool:
        variables = {"artistId": str(id)}

        response = self._request_graphql(GRAPHQL_IS_ARTIST_FAVORITE, variables)
        return response["artist"]["isFavorite"]

    def is_album_favorited(self, id: Union[str, int]) -> bool:
        variables = {"albumId": str(id)}

        response = self._request_graphql(GRAPHQL_IS_ALBUM_FAVORITE, variables)
        return response["album"]["isFavorite"]

    # Playlist send isFavorite through the gw

    def get_favorited_track_ids(self):
        data = self._get_api(METHOD_GET_FAVORITE_TRACKS)
        favorited_tracks: Dict[str, datetime] = {}

        for favorite in data["data"]:
            favorited_tracks[favorite["SNG_ID"]] = datetime.fromtimestamp(
                favorite["DATE_FAVORITE"]
            )

        return favorited_tracks

    def add_favorite_tracks(self, ids: ArrayLike[str]):
        now = datetime.now()

        json_data = {"IDS": ids}
        self._get_api(METHOD_ADD_FAVORITE_TRACKS, json_data)

        for id in ids:
            self.favorited_ids[id] = now

    def remove_favorite_tracks(self, ids: ArrayLike[str]):
        json_data = {"IDS": ids}
        self._get_api(METHOD_REMOVE_FAVORITE_TRACKS, json_data)

        for id in ids:
            if id not in self.favorited_ids:
                continue
            del self.favorited_ids[id]

    def add_favorite_album(self, id: str):
        variables = {"albumId": id}
        self._request_graphql(GRAPHQL_ADD_ALBUM_FAVORITE, variables)

    def remove_favorite_album(self, id: str):
        variables = {"albumId": id}
        self._request_graphql(GRAPHQL_REMOVE_ALBUM_FAVORITE, variables)

    def add_favorite_artist(self, id: str):
        json_data = {"ART_ID": id}
        self._get_api(METHOD_ADD_FAVORITE_ARTIST, json_data)

    def remove_favorite_artist(self, id: str):
        json_data = {"ART_ID": id}
        self._get_api(METHOD_REMOVE_FAVORITE_ARTIST, json_data)

    def add_favorite_playlist(self, id: str):
        json_data = {"PLAYLIST_ID": id}
        self._get_api(METHOD_ADD_FAVORITE_PLAYLIST, json_data)

    def remove_favorite_playlist(self, id: str):
        json_data = {"PLAYLIST_ID": id}
        self._get_api(METHOD_REMOVE_FAVORITE_PLAYLIST, json_data)

    def search(self, query: str):
        variables = {
            "channelPlaylistFirst": 10,
            "firstGrid": 10,
            "firstList": 6,
            "includeRelatedContent": True,
            "query": query,
        }
        return self._request_graphql(GRAPHQL_SEARCH, variables)

    def get_profile_page_tab(self, tab: str, id: str):
        json_data = {"nb": 10000, "tab": tab, "user_id": id}
        data = self._get_api(METHOD_GET_USER_PROFILE, json_data)

        return data
