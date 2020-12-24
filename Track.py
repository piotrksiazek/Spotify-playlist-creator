from spotipy import Spotify


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