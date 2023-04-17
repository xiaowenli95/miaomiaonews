# -*- encoding: utf-8 -*-
#%%
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string
from pydantic import BaseSettings, Field, validator
from typing import Optional


class FlaskConfig(BaseSettings):

    ASSETS_ROOT: str = Field(..., env='ASSETS_ROOT')
    SECRET_KEY: Optional[str] = Field(deafult=None, env='SECRET_KEY')
    SOCIAL_AUTH_GITHUB: bool = Field(default=False, env='SOCIAL_AUTH_GITHUB')
    GITHUB_ID: Optional[str] = Field(default=None, env='GITHUB_ID')
    GITHUB_SECRET: Optional[str] = Field(default=None, env='GITHUB_SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = Field(default=False, env='SQLALCHEMY_TRACK_MODIFICATIONS')
    USE_SQLITE: bool = Field(default=True, env='USE_SQLITE')
    SQLALCHEMY_DATABASE_URI: Optional[str] = Field(default=None, env='SQLALCHEMY_DATABASE_URI')

    @validator('SQLALCHEMY_DATABASE_URI')
    def passwords_match(cls, v, values):
        if 'USE_SQLITE' in values and values['USE_SQLITE']:
            basedir = os.path.abspath(os.path.dirname(__file__))
            new_uri = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
            return new_uri
        else:
            return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
class ProductionFlaskConfig(FlaskConfig):

    DEBUG: bool = Field(default=False, env='DEBUG')
    SESSION_COOKIE_HTTPONLY: bool = Field(default=True, env='SESSION_COOKIE_HTTPONLY')
    REMEMBER_COOKIE_HTTPONLY: bool = Field(default=True, env='REMEMBER_COOKIE_HTTPONLY')
    REMEMBER_COOKIE_DURATION: int = Field(default=3600, env='REMEMBER_COOKIE_DURATION')

class DebugConfigFlask(FlaskConfig):

    DEBUG: bool = Field(default="True", env='DEBUG')

# Load all possible configurations
config_dict = {
    'Production': ProductionFlaskConfig,
    'Debug'     : DebugConfigFlask
}

# %%
