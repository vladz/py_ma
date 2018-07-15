from typing import Any, Dict

from py_ma import XMLSchema, fields, post_load


class HabraSchema(XMLSchema):
    title = fields.Str(required=True)
    link = fields.Str(required=True)
    description = fields.Str()
    user = fields.Str(required=True, data_key='dc:creator', attribute='name')
    dt = fields.DateTime(required=True, format='%a, %d %b %Y %H:%M:%S %Z',
                         data_key='pubDate', attribute='dt_create')
    category = fields.List(fields.Str(), attribute='tags', missing=[])


class HabraSchemaItem(XMLSchema):
    item = fields.Nested(HabraSchema, many=True)


class HabraSchemaChannel(XMLSchema):
    channel = fields.Nested(HabraSchemaItem)


class HabraSchemaRSS(XMLSchema):
    rss = fields.XMLNested(HabraSchemaChannel)

    @post_load
    def make_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data['rss']['channel']['item']
