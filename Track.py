from spotipy import Spotify
from typing import List
import random
import requests
import json

class Track:
    # @staticmethod
    # def get_the_least_popular_track_id(spotify: Spotify, artist_id: str, reverse: bool = False, return_all: bool = False):
    #     track_id_with_popularity = dict()
    #     albums = spotify.artist_albums(artist_id)['items']
    #     for album_index in range(len(albums)):
    #         album_id = albums[album_index]['id']
    #         tracks = spotify.album_tracks(album_id)['items']
    #         for track_index in range(len(tracks)):
    #             track_id = tracks[track_index]['id']
    #             track_popularity = spotify.track(track_id)['popularity']
    #             track_id_with_popularity[track_id] = track_popularity
    #     if return_all:
    #         return track_id_with_popularity
    #     if reverse:
    #         return max(track_id_with_popularity, key=lambda key: track_id_with_popularity[key])
    #     return min(track_id_with_popularity, key=lambda key: track_id_with_popularity[key])

    @staticmethod
    def get_the_least_popular_track_id(spotify: Spotify, artist_id: str):

        albums = spotify.artist_albums(artist_id)['items']
        tracks_with_popularity = []
        for album_index in range(len(albums)):
            album_id = albums[album_index]['id']
            tracks = spotify.album_tracks(album_id)['items']
            for track_index in range(len(tracks)):
                track_id = tracks[track_index]['id']
                track_popularity = spotify.track(track_id)['popularity']
                tracks_with_popularity.append(tuple([track_id, track_popularity]))
        return sorted(tracks_with_popularity, key=lambda x: x[1])[0][0]

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
    def get_lyrics(artist: str, track_name: str) -> str:
        url = 'https://api.lyrics.ovh/v1/' + artist + '/' + track_name
        response = requests.get(url)
        json_data = json.loads(response.content)
        lyrics = json_data['lyrics']
        if not lyrics:
            lyrics = "Lyrics not found."
        return lyrics

    @staticmethod
    def get_discography_audiodb(artist_id: str) -> List[dict]:
        url = 'http://theaudiodb.com/api/v1/json/1/album.php?i=' + artist_id
        response = requests.get(url)
        json_data = json.loads(response.content)
        return json_data['album']

    @staticmethod
    def get_artist_info_audiodb(artist: str) -> dict:
        result = {}
        url = 'http://theaudiodb.com/api/v1/json/1/search.php?s=' + artist
        response = requests.get(url)
        json_data = json.loads(response.content)['artists'][0]
        result['id'] = json_data['idArtist']
        result['genre'] = json_data['strGenre']
        result['style'] = json_data['strStyle']
        result['formed_year'] = json_data['intFormedYear']
        result['artist banner'] = json_data['strArtistBanner']
        result['artist_bio'] = json_data['strBiographyEN']
        result['mood'] = json_data['strMood']
        result['website'] = json_data['strWebsite']
        result['facebook'] = json_data['strFacebook']
        result['twitter'] = json_data['strTwitter']
        result['number of members'] = json_data['intMembers']
        result['country'] = json_data['strCountry']
        result['discography'] = Track.get_discography_audiodb(result['id'])
        return result

    @staticmethod
    def get_track_info(spotify: Spotify, track_id: str) -> dict:
        result = {}
        track = spotify.track(track_id)
        milliseconds = track['duration_ms']
        seconds = int((milliseconds/1000)%60)
        minutes = int((milliseconds / (1000 * 60)) % 60)
        result['artist'] = track['artists'][0]['name']
        result['name'] = track['name']
        result['image'] = track['album']['images'][1]['url']
        result['id'] = track['id']
        result['duration'] = {'minutes': minutes, 'seconds': seconds}
        result['popularity'] = track['popularity']
        result['release_date'] = track['album']['release_date']
        result['explicit'] = track['explicit']
        try:
            result['lyrics'] = Track.get_lyrics(result['artist'], result['name'])
        except json.decoder.JSONDecodeError:
            result['lyrics'] = 'Lyrics not found.'
        if not result['lyrics']:
            result['lyrics'] = 'Lyrics not found.'
        return result

