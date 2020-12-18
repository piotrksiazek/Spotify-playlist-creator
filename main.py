import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import config

from Playlist import Playlist

scope = config.scope
my_uri = config.my_uri
user = config.user
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

old_playlist_id = 'spotify:playlist:2oHKnV8uHRPIyysDn5SjL0'


def create_new_playlist_from_not_mentioned_top_songs():
    new_playlist_id = Playlist.get_id_of_newest_playlist(spotify)
    artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)
    tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
    new_track_list = Playlist.get_new_listed_top_tracks(spotify, artists_from_old_playlist, tracks_from_old_playlist)
    spotify.user_playlist_add_tracks(user=user, playlist_id=new_playlist_id, tracks=new_track_list)


def create_new_playlist_from_corresponding_random_tracks():
    new_playlist_id = Playlist.get_id_of_newest_playlist(spotify)
    tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
    artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)
    new_track_list = Playlist.get_non_popular_tracks(spotify, artists_from_old_playlist, tracks_from_old_playlist)
    spotify.user_playlist_add_tracks(user=user, playlist_id=new_playlist_id, tracks=new_track_list)


def create_new_hipster_playlist():
    new_playlist_id = Playlist.get_id_of_newest_playlist(spotify)
    tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
    artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)

# print(spotify.album_tracks('spotify:album:0qZTwrunzX3LG45PvRghmh')['items'][0]['id'])
# print(spotify.track('3bWGaqVeYKMlLss40mPgNn')['popularity'])


album_id = spotify.artist_albums('spotify:artist:7M1FPw29m5FbicYzS2xdpi')['items'][0]['id']
tracks = spotify.album_tracks(album_id)['items'][0]['id']
pop = spotify.track(tracks)['popularity']
print(pop)

print(Playlist.get_least_popular_track(spotify, 'spotify:artist:3vWL2MmOBNpJAP2tw1TLQw'))