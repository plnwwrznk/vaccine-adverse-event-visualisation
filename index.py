"""
Index of available apps as required by gunicorn
"""

from source.main import app

app = app.server

if __name__ == "__main__":
    app.run()
