#%%
import re
import sys
import pandas as pd
import xml.etree.ElementTree as ET

from urllib.request import urlopen
from urllib.parse import quote
from typing import List
from loguru import logger

class WikiNews:

    language = None
    url = None


    def set_language_url(self, language: str) -> str:
        assert language in ["zh", "en"]
        self.url = f"https://{language}.wikipedia.org/"

    # TODO: set up retry
    def get_reivisions_xml(self, page_title: str) -> list:
        """https://stackoverflow.com/questions/34411896/how-to-get-full-wikipedia-revision-history-list-from-some-article
        """

        # quote zh character
        # https://stackoverflow.com/questions/4389572/how-to-fetch-a-non-ascii-url-with-urlopen
        revision_query_url = self.url + "w/api.php?action=query&format=xml&prop=revisions&rvlimit=500&titles=" + quote(page_title)
        revisions = []                                        #list of all accumulated revisions
        next = ''                                             #information for the next request
        while True:
            response = urlopen(revision_query_url + next).read().decode('utf-8')     #web request
            revisions += re.findall('<rev [^>]*>', response)  #adds all revisions from the current request to the list

            cont = re.search('<continue rvcontinue="([^"]+)"', response)
            if not cont:                                      #break the loop if 'continue' element missing
                break

            next = "&rvcontinue=" + cont.group(1)             #gets the revision Id from which to start the next request

        return revisions
    
    def parse_xml_to_pd_df(self, xml_list: List[str]) -> pd.DataFrame:

        data = []

        for row in xml_list:
            try:
                element = ET.fromstring(row)
                attributes = element.attrib
                data.append(attributes)
            except Exception as e:
                logger.error(e)

        return pd.DataFrame(data)

#%%
if __name__ == "__main__":

    logger.remove()
    # Set logging level to INFO and above
    logger.add(sys.stderr, format = "{time:HH:mm:ss.SS} | {file} took {elapsed} to execute | {level} | {message} ", level = "INFO")

    my_wiki = WikiNews()
    my_wiki.set_language_url("zh")
    l = my_wiki.get_reivisions_xml("丰县生育八孩女子事件")
    df = my_wiki.parse_xml_to_pd_df(l)
# %%
