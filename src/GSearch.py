#%%
# google search api
import requests
import json
import sys

from pydantic import BaseSettings, Field
from loguru import logger

class GSearchSetting(BaseSettings):

    api_key: str = Field(..., env='GOOGLE_SEARCH_KEY')
    search_engine_tag: str = Field(..., env='GOOGLE_SEARCH_ENGINE_TAG')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class GSearch:

    url = "https://www.googleapis.com/customsearch/v1"
    api_key = None
    search_engine_tag = None

    def __init__(self, settings: GSearchSetting):
        self.api_key = settings.api_key
        self.search_engine_tag = settings.search_engine_tag

    def search_by_query(self, query: str):

        # https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
        params = {
            "key": self.api_key,
            "cx": self.search_engine_tag,
            "q": query
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()

            json_result = response.json()
            logger.debug(json_result)
            return json_result
        except json.JSONDecodeError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)

         

#%%
if __name__ == "__main__":

    logger.remove()
    # Set logging level to INFO and above
    logger.add(sys.stderr, format = "{time:HH:mm:ss.SS} | {file} took {elapsed} to execute | {level} | {message} ", level = "INFO")

    settings = GSearchSetting()
    my_search = GSearch(settings)
    #my_search.search_by_query("baidu")
# %%
