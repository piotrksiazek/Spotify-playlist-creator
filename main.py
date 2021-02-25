import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import config

from Playlist import Playlist
from Track import Track

scope = config.scope
my_uri = config.my_uri
user = config.user
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def create_new_playlist_from_not_mentioned_top_songs(spot, old_playlist_id, new_playlist_id):
    # new_playlist_id = Playlist.get_id_of_newest_playlist(spotify)
    artists_from_old_playlist = Playlist.get_playlist_items(spot, old_playlist_id, 'artist', unique=True)
    tracks_from_old_playlist = Playlist.get_playlist_items(spot, old_playlist_id, 'track', unique=False)
    new_track_list = Playlist.get_non_popular_tracks(spot, artists_from_old_playlist, tracks_from_old_playlist)
    spot.user_playlist_add_tracks(user=user, playlist_id=new_playlist_id, tracks=new_track_list)


# def create_new_playlist_from_corresponding_random_tracks():
#     new_playlist_id = Playlist.get_id_of_newest_playlist(spotify)
#     tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
#     artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)
#     new_track_list = Playlist.get_non_popular_tracks(spotify, artists_from_old_playlist, tracks_from_old_playlist)
#     spotify.user_playlist_add_tracks(user=user, playlist_id=new_playlist_id, tracks=new_track_list)
#
#
# def create_new_hipster_playlist():
#     new_playlist_id = Playlist.get_id_of_newest_playlist(spotify)
#     tracks_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'track', unique=False)
#     artists_from_old_playlist = Playlist.get_playlist_items(spotify, old_playlist_id, 'artist', unique=True)


# print(spotify.album_tracks('spotify:album:0qZTwrunzX3LG45PvRghmh')['items'][0]['id'])
# print(spotify.track('3bWGaqVeYKMlLss40mPgNn')['popularity'])


# album_id = spotify.artist_albums('spotify:artist:7M1FPw29m5FbicYzS2xdpi')['items'][0]['id']
# tracks = spotify.album_tracks(album_id)['items'][0]['id']
# pop = spotify.track(tracks)['popularity']
# print(pop)

# id = Track.get_the_least_popular_track_id(spotify, 'spotify:artist:3vWL2MmOBNpJAP2tw1TLQw', reverse=True)
# print(spotify.track(id)['popularity'])

# create_new_playlist_from_corresponding_random_tracks()
# artist_id = 'spotify:artist:3Ya6VPgR8fqYmPsvA4Icpo'
# top_track = spotify.artist_top_tracks(artist_id)['tracks'][0]['popularity']
# print(top_track)
#
# track_id = Track.get_the_least_popular_track_idd(spotify, artist_id, 100)
# print(spotify.track(track_id)['name'])
# seed_tracks = ['spotify:track:0tIozUXiPiaFkaEFXSNo4L']
# recommendations = spotify.recommendations(seed_tracks=seed_tracks, limit=5)
# for i in range(len(recommendations['tracks'])):
#     print(recommendations['tracks'][i]['name'] + ' ' + str(recommendations['tracks'][i]['popularity']) + ' ' + recommendations['tracks'][i]['album']['artists'][0]['name'])
#
# track = Track.get_recommended_track(spotify, seed_tracks, 10)
# name = spotify.track(track[0])['name']
# print(name)

# print(spotify.playlist_items('spotify:playlist:0hCXmoLAFhxr2XI2RwEdg8')['items'][0]['track']['id'])

# print(Track.get_random_track_id_from_album(spotify=spotify, album_id='spotify:album:48XbS5emhKTYTw7YAiqUKL'))
# track = Track.get_info_about_track(spotify, 'spotify:track:63PEsIWyy3QgiPy4u5I9pG')
# for key, value in track.items():
#     print(key)
#     print(value)
#     print("\n\n--------------------------------------------------------------------------------\n\n")
# tracks = Playlist.get_deep_recommendations(spotify=spotify, user_id='rbegouu2bjgv6t268sa2dc9hj',
#                                            seed_tracks=['12iOM7n1XHIdxK1fRBJMs7', '0mkV15zALtx0qsKKYGyX4X', '1QtdHvQeFgSE7R7AuLPccZ'],
#                                            seed_genres=['alternative'], min_depth=5, size=10)

# genre_list = spotify.recommendation_genre_seeds()['genres']
# print(genre_list)

# tracks = spotify.recommendations(seed_genres=['anime'], seed_tracks=['spotify:track:4udBY8ZAsfQOjvdc0STCqb', '12iOM7n1XHIdxK1fRBJMs7'])
# print(tracks)

# playlist = spotify.playlist_items('spotify:playlist:5d9TmU4l2KyHxxGqJudSVA')['items']
# print(playlist)