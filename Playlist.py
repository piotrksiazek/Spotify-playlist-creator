from typing import List
from spotipy import Spotify
import random


class Playlist:

    @staticmethod
    def get_playlist_items(spotify: Spotify, playlist_id: str, type_of_item: str, unique: bool) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param playlist_id: playlist id
        :param type_of_item: 'artist' if desired items are artists and 'track' if they are tracks
        :param unique: if True returned list is unique, if False list can contain duplicates
        :returns: unique list of artists from playlist or list of all tracks
        """
        playlist = spotify.playlist_items(playlist_id)
        items_from_playlist = []
        if type_of_item == 'artist':
            for index, item in enumerate(playlist['items']):
                artist = playlist['items'][index]['track']['album']['artists'][0]['id']
                items_from_playlist.append(artist)
        elif type_of_item == 'track':
            for index, item in enumerate(playlist['items']):
                artist = playlist['items'][index]['track']['id']
                items_from_playlist.append(artist)

        return list(set(items_from_playlist)) if unique else items_from_playlist

    @staticmethod
    def get_id_of_newest_playlist(spotify: Spotify) -> str:
        """
        :param spotify: spotipy.Spotify class instance
        :returns: if of the most recently created playlist
        """
        new_playlist = spotify.current_user_playlists(limit=1, offset=0)
        return new_playlist['items'][0]['id']

    @staticmethod
    def get_corresponding_top_tracks(spotify: Spotify, artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param artists_id_list: List of artists' ids
        :param tracks_from_old_playlist: List of tracks' ids from a playlist we we want to base the action on
        :returns: list of found track ids
        """
        track_list = []
        for artist_id in artists_id_list:
            top_tracks = spotify.artist_top_tracks(artist_id, country='PL')['tracks']
            top_tracks_length = len(top_tracks)
            for track_index in range(top_tracks_length):
                track_id = top_tracks[track_index]['id']
                if track_id in tracks_from_old_playlist:
                    continue  # We don't want duplicates
                else:
                    track_list.append(track_id)
                    break  # We want only one corresponding track
        return track_list

    @staticmethod
    def get_non_popular_tracks(spotify: Spotify, artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]:
        """
        :param spotify: spotipy.Spotify class instance
        :param artists_id_list: List of artists' ids
        :param tracks_from_old_playlist: List of tracks' ids from a playlist we we want to base the action on
        :returns: list of corresponding track ids that are not listed in top artist's songs, chosen randomly
        """
        track_list = []
        for artist_index, artist_id in enumerate(artists_id_list):
            while True:
                albums = spotify.artist_albums(artist_id)['items']
                number_of_albums = len(albums)
                random_album_index = random.randint(0, number_of_albums - 1)
                random_album_id = albums[random_album_index]['id']
                random_album = spotify.album_tracks(random_album_id)['items']
                number_of_tracks = len(random_album)
                random_track_index = random.randint(0, number_of_tracks - 1)
                random_track_id = random_album[random_track_index]['id']

                if random_track_id in tracks_from_old_playlist:  # We didn't find anything new
                    continue
                else:
                    track_list.append(random_track_id)
                    break
        return track_list

    @staticmethod
    def create_new_playlist(spotify: Spotify, name: str, user: str):
        """Just a wrapper around already existing spotipy function"""
        spotify.user_playlist_create(user=user, name=name)

    @staticmethod
    def get_hipster_tracks(spotify: Spotify, artists_id_list: List[str], tracks_from_old_playlist: List[str]) -> List[str]:
        pass

    @staticmethod
    def is_playlist_name_unique(spotify: Spotify, playlist_name: str, user: str) -> bool:
        playlists = spotify.user_playlists(user)['items']
        for i in range(len(playlists)):
            if playlists[i]['name'] == playlist_name:
                return False
        return True




