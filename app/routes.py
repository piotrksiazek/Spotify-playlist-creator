from flask import render_template, redirect, url_for, request, session
import spotipy
from app.forms import OriginDestination, OriginDestination2, LoginForm, RegistrationForm, CreateNewPlaylist, DeleteUserPlaylist, TrackId, ArtistId
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import models
from app import db
from app import spotify, user
from Playlist import Playlist
from Track import Track
from main import create_new_playlist_from_not_mentioned_top_songs


@app.login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ""
    try:
        #in case current user has not registered a new accound during this session
        registered = session['registered']
    except KeyError:
        registered = ''

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_object = models.User.query.filter_by(username=form.username.data).first()
        if user_object is None or not user_object.check_password(form.password.data):
            error_message = 'Invalid username or password'
        else:
            login_user(user_object, remember=form.remember_me.data)
            session['registered'] = ''
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, error_message=error_message, registered=registered)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_object = models.User(username=form.username.data, email=form.email.data, spotify_id=form.spotify_id.data)
        user_object.set_password(form.password.data)
        db.session.add(user_object)
        db.session.commit()
        session['registered'] = f'Welcome {form.username.data}. You can now login.'
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/my_items', methods=['GET', 'POST'])
@login_required
def my_items():
    user_playlists = models.UserPlaylist.query.filter_by(user_id=current_user.id).all()
    print('xD')
    user_playlists_dict_list = []
    for playlist in user_playlists:
        playlist_response = spotify.playlist(playlist.playlist_id)
        playlist_dict = {'name': playlist.playlist_name,
                         'link': playlist_response['external_urls']['spotify']}
        user_playlists_dict_list.append(playlist_dict)
    create_form = CreateNewPlaylist()
    delete_form = DeleteUserPlaylist()
    delete_form.user_playlist.choices = [playlist.playlist_name for playlist in user_playlists if playlist.user_id == current_user.id]
    is_unique = True
    number_of_user_playlists = 0
    if create_form.validate_on_submit():
        name = create_form.playlist_name.data
        is_unique = Playlist.is_playlist_name_unique(spotify, name, user)
        number_of_user_playlists = len(models.UserPlaylist.query.filter_by(user_id=current_user.id).all())
        if is_unique and number_of_user_playlists < 3:
            Playlist.create_new_playlist(spotify=spotify, name=name, user=user)
            playlist = models.UserPlaylist(playlist_name=name, playlist_id=Playlist.get_playlist_id_with_name(spotify, name, user), user=current_user)
            db.session.add(playlist)
            db.session.commit()

    if delete_form.validate_on_submit():
        playlist_to_clear = models.UserPlaylist.query.filter_by(playlist_name=delete_form.user_playlist.data).first().playlist_id
        Playlist.clear_playlist(spotify=spotify, playlist_id=playlist_to_clear, user=user)
    return render_template('my_items.html', form=create_form, up=user_playlists_dict_list, delete_form=delete_form,
                           is_unique=is_unique, number_of_user_playlists=number_of_user_playlists)


@app.route('/mirror', methods=['GET', 'POST'])
@login_required
def mirror():
    current_user_hosted_playlists = models.UserPlaylist.query.filter_by(user_id=current_user.id).all()
    playlists_dict = {}
    for playlist in spotify.user_playlists(current_user.spotify_id)['items']:
        playlists_dict[playlist['name']] = playlist['id']
    playlists_names = [name for name, name_id in playlists_dict.items()]
    form = OriginDestination2()
    # User can only manipulate playlists that belong to him
    form.destination_playlist.choices = [playlist.playlist_name for playlist in current_user_hosted_playlists if playlist.user_id == current_user.id]
    form.origin_playlist.choices = playlists_names

    if form.validate_on_submit():
        playlists_dict[form.destination_playlist.data] = Playlist.get_playlist_id_with_name(spotify, form.destination_playlist.data, user)
        Playlist.create_new_playlist_from_not_mentioned_songs(spotify, playlists_dict[form.origin_playlist.data],
                                                         playlists_dict[form.destination_playlist.data])
    return render_template('mirror.html', playlists=playlists_names, form=form)

@app.route('/one_album_one_track', methods=['GET', 'POST'])
@login_required
def one_album_one_track():
    user_playlists = models.UserPlaylist.query.filter_by(user_id=current_user.id).all()
    form = OriginDestination()
    form.destination_playlist.choices = [user_playlist.playlist_name for user_playlist in user_playlists if user_playlist.user_id == current_user.id]
    error_message = ""
    if form.validate_on_submit():
        try:
            track_ids = Playlist.get_random_track_from_each_album(spotify, form.artist.data)
            playlist_id = models.UserPlaylist.query.filter_by(playlist_name=form.destination_playlist.data).first().playlist_id
            spotify.playlist_add_items(playlist_id, track_ids)
        except spotipy.exceptions.SpotifyException:
            error_message = "Wrong ID, maybe you pasted track id instead of artist id?"

    return render_template('one_album_one_track.html', form=form, error_message=error_message)

@app.route('/get_least_popular_track', methods=['GET', 'POST'])
@login_required
def get_least_popular_track():
    form = ArtistId()
    track_id = ""
    error_message = ""
    if form.validate_on_submit():
        artist_id = form.artist_id.data
        try:
            track_id = Track.get_the_least_popular_track_id(spotify, artist_id)
        except spotipy.exceptions.SpotifyException:
            error_message = "Wrong ID"
    return render_template('least_popular_track.html', form=form, track_id=track_id, error_message=error_message)

@app.route('/all_about_that_track', methods=['GET', 'POST'])
@login_required
def all_about_that_track():
    form = TrackId()
    audio_features = {}
    track = {}
    artist = {}
    error_message = ""
    audiodb_error = ""
    if form.validate_on_submit():
        try:
            audio_features = Track.get_audio_features(spotify, form.track_id.data)
            track = Track.get_track_info(spotify, form.track_id.data)
            try:
                artist = Track.get_artist_info_audiodb(track['artist'])
            except TypeError:
                audiodb_error = "Couldn't find more complex data about artist."
        except spotipy.exceptions.SpotifyException:
            error_message = "Wrong ID"
    return render_template('all_about_that_track.html',
                           form=form, audio_features=audio_features, track=track, artist=artist,
                           error_message=error_message, audiodb_error=audiodb_error)

@app.route('/deep_recommendations', methods=['GET', 'POST'])
@login_required
def deep_recommendations():
    track_list = []
    error_message = ""
    current_user_hosted_playlists = models.UserPlaylist.query.filter_by(user_id=current_user.id).all()
    playlists_dict = {}
    for playlist in spotify.user_playlists(current_user.spotify_id)['items']:
        playlists_dict[playlist['name']] = playlist['id']
    playlists_names = [name for name, name_id in playlists_dict.items()]
    form = OriginDestination2()
    # User can only manipulate playlists that belong to him
    form.destination_playlist.choices = [playlist.playlist_name for playlist in current_user_hosted_playlists if
                                         playlist.user_id == current_user.id]
    form.origin_playlist.choices = playlists_names
    if form.validate_on_submit():
        if not spotify.playlist_items(playlists_dict[form.origin_playlist.data])['items']:
            error_message = "Origin playlist can't be empty."
            return render_template('deep_recommendations.html', form=form, error_message=error_message)
        playlist_items = spotify.playlist_items(playlists_dict[form.origin_playlist.data])['items']
        for track in playlist_items:
            track_dict = {"name": track['track']['name'], "id": track['track']['id'],
                          "artist": track['track']['artists'][0]['name'], "artist_id": track['track']['artists'][0]['id']}
            track_list.append(track_dict)
        session['track_list'] = track_list
        session['destination_playlist'] = models.UserPlaylist.query.filter_by(user_id=current_user.id, playlist_name=form.destination_playlist.data).first().playlist_id
        return redirect(url_for('seed'))

    return render_template('deep_recommendations.html', form=form)

@app.route('/deep_recommendations/seed', methods=['GET', 'POST'])
@login_required
def seed():
    track_list = session['track_list']
    genre_list = spotify.recommendation_genre_seeds()['genres']

    destination_playlist = session['destination_playlist']

    if request.method == 'POST':
        seed_tracks = request.form.getlist('seed')
        seed_genres = [request.form.get('genre')]
        depth = int(request.form.get('depth'))
        size = int(request.form.get('size'))
        print(seed_genres)
        if seed_tracks or seed_genres:
            track_ids = Playlist.get_deep_recommendations(spotify, current_user.spotify_id,
                                                          seed_tracks, seed_genres, depth, size)
            spotify.playlist_add_items(destination_playlist, track_ids)
            return redirect(url_for('deep_recommendations'))
    return render_template('seed.html', track_list=track_list, genre_list=genre_list)

@app.route('/actions')
@login_required
def actions():
    return render_template('Actions.html')


if __name__ == '__main__':
    app.run(debug=True)
