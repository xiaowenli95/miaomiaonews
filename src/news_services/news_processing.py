
from newspaper import Article

def news_emmit_digests(
    url: str,
    digests: list = ["authors", "publish_date", "keywords", "summary"],
    language: str = "zh"
    ):

    article = Article(url, language=language)
    article.download()
    article.parse()
    
    try:
        article.nlp()
    except:
        import nltk
        nltk.download('punkt')
        article.enlp()
    
    article_digests = {}
    for digest_attribute in digests:
        attr_value = getattr(article, digest_attribute)
        article_digests[digest_attribute] = attr_value

    return article_digests