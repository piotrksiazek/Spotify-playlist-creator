from typing import List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
import pprint
scope = "playlist-modify-public"
my_uri = 'spotify:playlist:1qBB4GjHyKZYnQclPJfNe0'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# 'spotify:playlist:1jfYYhj3hvaKkxilBvgx5l'
pp = pprint.PrettyPrinter(indent=4)
user='rbegouu2bjgv6t268sa2dc9hj'


def get_playlist_items(playlist_id: str, type_of_item: str) -> List[str]:
    playlist = spotify.playlist_items(playlist_id)
    artists_from_playlist = []
    if type_of_item == 'artist':
        for index, item in enumerate(playlist['items']):
            artist = playlist['items'][index]['track']['album']['artists'][0]['id']
            artists_from_playlist.append(artist)
        return list(set(artists_from_playlist))
    elif type_of_item == 'track':
        for index, item in enumerate(playlist['items']):
            artist = playlist['items'][index]['track']['id']
            artists_from_playlist.append(artist)
        return artists_from_playlist

def create_new_playlist(name: str):
    spotify.user_playlist_create(user=user, name=name)

def get_id_of_newest_playlist() -> str:
    new_playlist = spotify.current_user_playlists(limit=1, offset=0)
    return new_playlist['items'][0]['id']


def get_new_track_list(artists_id_list: List[str], tracks_from_old_playlist: List[str]):
    track_list = []
    for artist_id in artists_id_list:
        top_tracks = spotify.artist_top_tracks(artist_id, country='US')
        for track in top_tracks:
            pass

def create_list_of_tracks(playlist_id: str, tracks: List[str]) -> List[str]:
    pass




#
# sp.user_playlist_add_tracks(user=user, playlist_id=playlist_id, tracks=['spotify:track:6OQCLaG8vDoRcgi7vzYEQK'])
old_playlist_id = 'spotify:playlist:2Pcd729IGTgs9QfkA7kjqe'
def main():
    # create_new_playlist('nowa_playlista')
    new_playlist_id = get_id_of_newest_playlist()
    artists_from_old_playlist = get_playlist_items(new_playlist_id, 'artist')
    tracks_from_old_playlist = get_playlist_items(old_playlist_id, 'track')
    print(tracks_from_old_playlist)

main()