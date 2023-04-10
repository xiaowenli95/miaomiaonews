#%%
# google search api
import requests
import json
import sys, os
import pandas as pd

from pydantic import BaseSettings, Field
from loguru import logger
from typing import Dict, Type
from pathlib import Path

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

    def search_result_by_query(self, query: str, timeframe: str = "d7"):
        """timeframe can be d1/w1/m1/y1 or d[number]
        """
        # https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
        params = {
            "key": self.api_key,
            "cx": self.search_engine_tag,
            "q": query,
            "dateRestrict": timeframe
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

    def export_json_result(
            self,
            json_input: Type[Dict], 
            export_path: Path = os.getcwd(), 
            file_name: str = "data.json"
            ):

        file_name = file_name
        file_path = Path(export_path) / file_name
        # Fix Chinese character export
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_input, f, ensure_ascii=False)

    def parse_reponse_json_to_pd_df(self, json_input: Type[Dict]) -> pd.DataFrame:
    
        cols = ["title", "link", "snippet", "htmlSnippet"]
        df = pd.json_normalize(json_input, record_path =['items'])
        df = df[cols].copy()
        
        return df


#%%
if __name__ == "__main__":

    logger.remove()
    # Set logging level to INFO and above
    logger.add(sys.stderr, format = "{time:HH:mm:ss.SS} | {file} took {elapsed} to execute | {level} | {message} ", level = "INFO")

    settings = GSearchSetting()
    my_search = GSearch(settings)
    json_input = my_search.search_result_by_query("丰县八孩")
    #my_search.export_json_result(json_input)
    df = my_search.parse_reponse_json_to_pd_df(json_input)
# %%
