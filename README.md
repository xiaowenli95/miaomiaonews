# miaomiaonews
Have you always tried to follow a news topic only to find that eventually it will be shoved to a pile of **many** new topics. miaomiaonews help you follow a news topic with the latest development from today!

## Overview of the workflow
The application will search the topic (as in google search query) you entered on google. Then a summary will be delivered by [newspaper](https://github.com/codelucas/newspaper). Finally a digest will be prepared by ChatGPT.

## Env
- Recommended to use pyenv to manage different versions of python
- Install poetry to manage python library dependencies
- Settings must be included in the dotenv file at the project root path
    - GOOGLE_SEARCH_KEY: your registered google search engine
    - GOOGLE_SEARCH_ENGINE_TAG: tag of the created engine
    - OPENAI_API_KEY: ChatGPT key from OpenAI

## Test
You should be able to run `news_digest_on_topic_creation.py` successfully. 
