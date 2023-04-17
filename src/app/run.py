# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from src.app.webapp.config import config_dict
from src.app.webapp import create_app, db

settings = config_dict['Debug']()
app = create_app(settings)
Migrate(app, db)

if __name__ == "__main__":
    app.run()
