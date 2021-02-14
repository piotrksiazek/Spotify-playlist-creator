from spotipy import Spotify
from typing import List
import random

class Track:
    @staticmethod
    def get_the_least_popular_track_id(spotify: Spotify, artist_id: str, reverse: bool = False, return_all: bool = False):
        track_id_with_popularity = dict()
        albums = spotify.artist_albums(artist_id)['items']
        for album_index in range(len(albums)):
            album_id = albums[album_index]['id']
            tracks = spotify.album_tracks(album_id)['items']
            for track_index in range(len(tracks)):
                track_id = tracks[track_index]['id']
                track_popularity = spotify.track(track_id)['popularity']
                track_id_with_popularity[track_id] = track_popularity
        if return_all:
            return track_id_with_popularity
        if reverse:
            return max(track_id_with_popularity, key=lambda key: track_id_with_popularity[key])
        return min(track_id_with_popularity, key=lambda key: track_id_with_popularity[key])

    @staticmethod
    def get_the_least_popular_track_idd(spotify: Spotify, artist_id: str, accuracy: int, reverse: bool = False,
                                       return_all: bool = False):
        if reverse:
            return spotify.artist_top_tracks(artist_id)['tracks'][0]['id']
        track_id_with_popularity = dict()
        albums = spotify.artist_albums(artist_id)['items']
        max_popularity = spotify.artist_top_tracks(artist_id)['tracks'][0]['popularity']
        min_popularity = int(max_popularity/accuracy)
        for album_index in range(len(albums)):
            album_id = albums[album_index]['id']
            tracks = spotify.album_tracks(album_id)['items']
            for track_index in range(len(tracks)):
                track_id = tracks[track_index]['id']
                track_popularity = spotify.track(track_id)['popularity']
                track_id_with_popularity[track_id] = track_popularity
                if track_popularity <= min_popularity and not return_all:
                    return track_id
        if return_all:
            return track_id_with_popularity
        return min(track_id_with_popularity, key=lambda key: track_id_with_popularity[key])

    @staticmethod
    def get_recommended_track(spotify: Spotify, track_ids: List[str], depth: int, genres: List[str] = None) -> str:
        duplicates = []
        the_least_popular_track = str
        for i in range(depth):
            recommended_tracks = [(track['id'], track['popularity']) for track in spotify.recommendations(seed_tracks=(track_ids))['tracks']]
            sorted(recommended_tracks, key=lambda x: x[1])
            for j, track in enumerate(recommended_tracks):
                if track not in duplicates:
                    the_least_popular_track = track[j]
                    track_ids = [the_least_popular_track]
                    break
                duplicates.append(the_least_popular_track)
        print(duplicates)
        return the_least_popular_track

    @staticmethod
    def get_random_track_id_from_album(spotify: Spotify, album_id: str):
        items = spotify.album_tracks(album_id)['items']
        number_of_tracks = len(items)
        track_index = random.randint(0, number_of_tracks-1)
        return items[track_index]['id']

    @staticmethod
    def get_audio_features(spotify: Spotify, track_id: str) -> dict:
        return spotify.audio_features([track_id])[0]

    @staticmethod
    def get_track_info(spotify: Spotify, track_id: str) -> dict:
        result = {}
        track = spotify.track(track_id)
        result['artist'] = track['artists'][0]['name']
        result['name'] = track['name']
        result['image'] = track['album']['images'][1]['url']
        result['id'] = track['id']
        return result

