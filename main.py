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

playlists = spotify.user_playlists('dianazabiegla')
print(playlists['items'][0]['id'])