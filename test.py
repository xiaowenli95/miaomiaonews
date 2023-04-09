#%%
import pandas as pd
import duckdb
import sys, os

from newspaper import Article
from loguru import logger
from src.GSearch import GSearch, GSearchSetting
from src.news_processing import news_emmit_digests

 # %%
if __name__ == "__main__":

    logger.remove()
    # Set logging level to INFO and above
    logger.add(sys.stderr, format = "{time:HH:mm:ss.SS} | {file} took {elapsed} to execute | {level} | {message} ", level = "INFO")

    # Testing GSearch
    settings = GSearchSetting()
    my_search = GSearch(settings)
    json_input = my_search.search_result_by_query("丰县八孩")
    #my_search.export_json_result(json_input)
    df = my_search.parse_reponse_json_to_pd_df(json_input)

    # Testing news_processing
    digests = news_emmit_digests(df.loc[0]["link"])
    for row in df.itertuples(index=False):
        print(news_emmit_digests(row.link))

# %%
