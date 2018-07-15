import logging
from typing import Any, Dict, Iterator, Union

import requests

from .habra_config import HabraSchemaRSS
from .reddit_config import RedditSchemaRSS

logger = logging.getLogger(__name__)

_habra_schema = HabraSchemaRSS()
_reddit_schema = RedditSchemaRSS()

CONFIGS = {
    'habra': {'url': 'https://habr.com/rss/hubs/all/',
              'schema': _habra_schema},
    'reddit': {'url': 'https://www.reddit.com/r/news/.rss',
               'schema': _reddit_schema},
}

def load_rss(type: str) -> Union[Iterator[Dict[str, Any]], str]:
    rss_config = CONFIGS[type]
    response = requests.get(rss_config['url'])
    if response.status_code != requests.codes.ok:
        err = f'CODE: {response.status_code}\nMSG: {response.text}'
        logger.warning(err)
        return err
    return rss_config['schema'].loads(response.text)
