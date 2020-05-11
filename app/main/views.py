from flask import render_template, redirect, url_for

from . import main
from .forms import SpotifyForm
from .. import spotify
from .. import library


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SpotifyForm()
    if form.validate_on_submit():
        print("Button pressed")
        spotify_library = spotify.import_spotify_library()
        print(spotify_library)
        library.lib.refresh_from_spotify(spotify_library)
        return redirect(url_for('.index'))
    return render_template('index.html', form=form)
