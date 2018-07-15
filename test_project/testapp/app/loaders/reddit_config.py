from typing import Any, Dict, Iterator

from py_ma import XMLSchema, fields, post_load


class RedditSchemaAuthor(XMLSchema):
    name = fields.Str(required=True)


class RedditSchemaLink(XMLSchema):
    href = fields.Str(required=True, data_key='@href')


class RedditSchemaContent(XMLSchema):
    data = fields.Str(required=True, data_key='#text')


class RedditSchemaCategory(XMLSchema):
    cat = fields.Str(required=True, data_key='@term')


class RedditSchema(XMLSchema):
    title = fields.Str(required=True)
    author = fields.Nested(RedditSchemaAuthor, required=True)
    link = fields.Nested(RedditSchemaLink, required=True)
    description = fields.Nested(RedditSchemaContent, data_key='content')
    updated = fields.DateTime(required=True, attribute='dt_create')
    category = fields.XMLNested(RedditSchemaCategory, attribute='tags',
                                many=True)

    @post_load
    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tags = data.get('tags')
        if tags:
            tag_list = []
            for tag in tags:
                tag_list.append(tag['cat'])
            data['tags'] = tag_list
        return data


class RedditSchemaEntry(XMLSchema):
    entry = fields.XMLNested(RedditSchema, required=True, many=True)


class RedditSchemaRSS(XMLSchema):
    feed = fields.Nested(RedditSchemaEntry, required=True)

    @post_load
    def export_data(self, data: Dict[str, Any]) -> Iterator[Dict]:
        entry = data['feed']['entry']
        for row in entry:
            author = row.pop('author')
            row['name'] = author['name']
            row['description'] = row['description']['data']
            row['link'] = row['link']['href']
            yield row
