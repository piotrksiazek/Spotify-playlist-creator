# Spotify playlist creator

> Web application made with Python, Flask, SQLAlchemy, Spotipy and Bootstrap.
> Live version https://spotifycreator.herokuapp.com/

## Installation
---
```shell
$ cd your/desired/directory
$ git clone https://github.com/piotrksiazek/Spotify-playlist-creator.git
$ pip install -r requirements.txt
$ export SPOTIPY_CLIENT_ID='your_client_id'
$ export SPOTIPY_CLIENT_SECRET='your_client_secret'
$ export SPOTIPY_REDIRECT_URI='https://www.spotify.com/pl/'
$ export FLASK_APP='api.py'
$ flask run
```
* Go to actions
* Go to deep recommendations
* Follow the link that popped up in the terminal
* Copy and paste url you were redirected to in the terminal
* Ctrl + c to abort
```shell
$ flask run
```
---

Copy your localhost address from shell and you are now running local version of an app.

## Functionality

After installation you will need to make a new account using login, password, email and spotify ID.
When logged in you will be able to access functionalities. First step is to go to My Items tab and make a new playlist.
Then you can go to Actions and choose one of following:

* Mirror Playlist - select origin playlist that belongs to your personal Spotify account and select one of created playlists (theese are hosted on
my account but you are the only one that can modify them). After submitting, destination playlist will contain the same amount of songs and
matching artists, but with different tracks. For example if you have:
```
Stairway to heaven - Led Zeppelin
Little wing - Jimi Hendrix
```
The final playlist may look like:
```
No Quarter - Led Zeppelin
Purple Haze - Jimi Hendrix
```
* One track for one album - pretty self explanatory. You enter spotify artist id, select destination playlist and you get one track from each album.

* All about that track - enter spotify track ID and you will see pretty interesting information normally hidden by spotify, like audio characteristics.
You will also see discography with descriptions, lyrics, artist bio and a little playback addon. Note that obscure tracks may not return lyrics etc.

* Least popular track - enter spotify artist ID and you will get the least popular track from that artist. Popularity isn't based fully on number of views,
so the least popular track in spotify's sense may be not the least viewed.

* Deep recommendations - choose origin (from which you will take your seed) and destination playlist. Then select at most 5 songs and genres
and depth of search and server will find recommendations based on recommendations basend on recommendations etc. based on the depth you
have chosen.

One user can make no more than 3 playlists and they can't be deleted (thanks to spotify api) but you can delete tracks from them.
