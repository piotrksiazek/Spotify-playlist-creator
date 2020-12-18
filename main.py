from typing import List
import random
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


def get_playlist_items(playlist_id: str, type_of_item: str) -> List[str]: ###
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

def get_id_of_newest_playlist() -> str: ###
    new_playlist = spotify.current_user_playlists(limit=1, offset=0)
    return new_playlist['items'][0]['id']


def get_new_listed_top_tracks(artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]: ###
    track_list = []
    for artist_id in artists_id_list:
        top_tracks = spotify.artist_top_tracks(artist_id, country='PL')['tracks']
        top_tracks_length = len(top_tracks)
        for track_index in range(top_tracks_length):
            track_id = top_tracks[track_index]['id']
            if track_id in tracks_from_old_playlist:
                continue # We dont want duplicates
            else:
                track_list.append(track_id)
                break # We want only one corresponding track
    return track_list


def get_non_popular_tracks(artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]: ###
    track_list = []
    for artist_index, artist_id in enumerate(artists_id_list):
        while True:
            albums = spotify.artist_albums(artist_id)['items']
            number_of_albums = len(albums)
            random_album_index = random.randint(0, number_of_albums-1)
            random_album_id = albums[random_album_index]['id']
            random_album = spotify.album_tracks(random_album_id)['items']
            number_of_tracks = len(random_album)
            random_track_index = random.randint(0, number_of_tracks-1)
            random_track_id = random_album[random_track_index]['id']

            if random_track_id in tracks_from_old_playlist: #We didn't find anything new
                continue
            else:
                track_list.append(random_track_id)
                break
    return track_list


old_playlist_id = 'spotify:playlist:2oHKnV8uHRPIyysDn5SjL0'


def create_new_playlist_from_not_mentioned_top_songs():
    new_playlist_id = get_id_of_newest_playlist()
    artists_from_old_playlist = get_playlist_items(old_playlist_id, 'artist')
    tracks_from_old_playlist = get_playlist_items(old_playlist_id, 'track')
    new_track_list = get_new_listed_top_tracks(artists_from_old_playlist, tracks_from_old_playlist)
    spotify.user_playlist_add_tracks(user=user, playlist_id=new_playlist_id, tracks=new_track_list)


def create_new_playlist_from_corresponding_random_tracks():
    new_playlist_id = get_id_of_newest_playlist()
    # artists_from_old_playlist = get_playlist_items(old_playlist_id, 'artist')
    tracks_from_old_playlist = get_playlist_items(old_playlist_id, 'track')
    artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', True)
    new_track_list = get_non_popular_tracks(artists_from_old_playlist, tracks_from_old_playlist)
    spotify.user_playlist_add_tracks(user=user, playlist_id=new_playlist_id, tracks=new_track_list)

create_new_playlist_from_corresponding_random_tracks()