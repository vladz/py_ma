from typing import Any, Dict

from app.loaders import load_rss
from app.models import (db, create_or_get_one, get_one_or_create,
                        upsert, Author, Article, Tag, Source)


def save_to_db(source: str, data: Dict[str, Any]):
    if not data:
        return
    name = data.pop('name')
    tags = data.pop('tags')
    session = db.session()
    source = get_one_or_create(session, Source, name=source)
    author = create_or_get_one(session, Author, name=name)
    data['author_id'] = author.id
    article = upsert(session, Article, {'link': data['link']}, data)
    article.source_id = source.id
    new_tags = set()
    for tag in tags:
        tag = create_or_get_one(session, Tag, data=tag)
        new_tags.add(tag)
    article.tags = list(new_tags)
    session.flush()
    session.commit()


def import_rss_data(source: str):
    data = load_rss(source)
    if isinstance(data, str):
        return data
    for i in data:
        save_to_db(source, i)
