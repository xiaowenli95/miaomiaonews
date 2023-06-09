#%%
import pandas as pd
import duckdb
import sys, os

from newspaper import Article
from loguru import logger
from news_services.GSearch import GSearch, GSearchSetting
from news_services.news_processing import news_emmit_digests
from news_services.chatGPT_news import ChatGPTNews, ChatGPTNewsSettings

 # %%
if __name__ == "__main__":

    logger.remove()
    # Set logging level to INFO and above
    logger.add(sys.stderr, format = "{time:HH:mm:ss.SS} | {file} took {elapsed} to execute | {level} | {message} ", level = "INFO")

    search_key_word = "丰县八孩"

    # Testing GSearch
    settings = GSearchSetting()
    my_search = GSearch(settings)
    json_input = my_search.search_result_by_query(search_key_word)
    #my_search.export_json_result(json_input)
    df = my_search.parse_reponse_json_to_pd_df(json_input)

    # Testing news_processing
    #digests = news_emmit_digests(df.loc[0]["link"])
    keywords_gathering = []
    for row in df.itertuples(index=False):
        digest = news_emmit_digests(row.link)
        keywords = digest['keywords']
        longest_string = max(keywords, key=len)
        longest_string_truncated = longest_string[0:100]
        keywords_gathering.append(longest_string_truncated)

    # Testing chatGPT_news
    settings = ChatGPTNewsSettings()
    my_response = ChatGPTNews(settings)
    text = "Based on these records, give me a news update. Please deliver the response in simplied Chinese:" + \
        str(keywords_gathering)
    answer = my_response.one_off_response(text)
    logger.success(answer)

# %%
