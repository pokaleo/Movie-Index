"""
------------------------------------------------------------
Author: Leo LI
Date: 7th Mr 2023
Description: Gunicorn service serve as the web server
gateway interface
------------------------------------------------------------
"""

from routes import app


if __name__ == "__main__":
    app.run()
