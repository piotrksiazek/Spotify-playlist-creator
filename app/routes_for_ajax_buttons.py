from app import app
from Playlist import Playlist
from app import spotify, user
from flask import request

@app.route('/Ajax', methods=['GET', 'POST'])
def ajax_do():
    name = request.args.get('name')
    print("dziala")
    Playlist.create_new_playlist(spotify=spotify, name=name, user=user)
    return "Nothing"