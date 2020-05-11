import os

from dotenv import load_dotenv

from app import create_app
# from app.models import User, Role

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
