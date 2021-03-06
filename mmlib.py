import os

from dotenv import load_dotenv

from app import create_app, db
from app.models import Album, Artist, Playlist, Tag, Track

load_dotenv()
dev_mode = bool(os.getenv('MMLIB_DEV_MODE') == '1')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.logger.debug("app started")
app.logger.debug(f"dev mode: {dev_mode}")

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Album=Album, Artist=Artist, Playlist=Playlist, Tag=Tag, Track=Track)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
