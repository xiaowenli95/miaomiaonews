#%%

filename = "data.json"

# Open the file in write mode
with open(filename, 'w', encoding='utf8') as f:
    # Convert the dictionary
    json.dump(response.json(), f, ensure_ascii=False)


#%%
import pandas as pd
import duckdb

with open(filename, 'r') as f:
    raw = json.load(f)
df = pd.json_normalize(raw, record_path=['items'])
# %%
from newspaper import Article
url = "http://www.news.cn/2023-04/07/c_1129501525.htm"
article = Article(url, language='zh')
article.download()
article.parse()
article.authors
article.publish_date
article.text
import nltk
nltk.download('punkt')
article.nlp()
article.keywords
article.summary
# %%
