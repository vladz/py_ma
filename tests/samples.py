from py_ma import CSVSchema, XMLSchema, JSONSchema, fields, post_load

simple_dict = {'x': 123}
simple_json = '{"x": 123}'
simple_csv = 'x\n123'
simple_xml = '<x>123</x>'


class SimpleCSV(CSVSchema):
    x = fields.Int()


class SimpleXML(XMLSchema):
    x = fields.Int()


class SimpleJSON(JSONSchema):
    x = fields.Int()


complicated_dict = {
    'result_field1': 123,
    'result_field2': [1, 2, 3],
    'result_field3': [
        {
            'result_field4': 'eee',
            'result_field5': {
                'result_field6': [3, 2, 1]
            }
        }
    ]
}

complicated_json = '''{
    "X": 123,
    "Y": [1, 2, 3],
    "Z": [
        {
            "Q": "eee",
            "ddd": {
                "y": [3, 2, 1]
            }
        }
    ],
    "unwanted": {
        "zzz": "zzz"
    }
}'''

complicated_xml = '''
<root>
    <X>123</X>
    <Y>1</Y>
    <Y>2</Y>
    <Y>3</Y>
    <Z>
        <Q>eee</Q>
        <ddd>
                <y>3</y>
                <y>2</y>
                <y>1</y>
        </ddd>
    </Z>
    <unwanted>
        <zzz>zzz</zzz>
    </unwanted>
</root>
'''


class ComplicatedJSONNested2(JSONSchema):
    y = fields.List(fields.Int(), attribute='result_field6')


class ComplicatedJSONNested(JSONSchema):
    z1 = fields.Str(required=True, attribute='result_field4', data_key='Q')
    z2 = fields.Nested(ComplicatedJSONNested2,
                       attribute='result_field5', data_key='ddd')


class ComplicatedJSON(JSONSchema):
    r1 = fields.Int(required=True, attribute='result_field1', data_key='X')
    r2 = fields.List(fields.Int(), required=True,
                     attribute='result_field2', data_key='Y')
    nested = fields.Nested(ComplicatedJSONNested, many=True,
                           attribute='result_field3', data_key='Z')


class ComplicatedXMLNested3(JSONSchema):
    y = fields.List(fields.Int(), attribute='result_field6')


class ComplicatedXMLNested2(JSONSchema):
    z1 = fields.Str(required=True, attribute='result_field4', data_key='Q')
    z2 = fields.XMLNested(ComplicatedXMLNested3,
                       attribute='result_field5', data_key='ddd')


class ComplicatedXMLNested(XMLSchema):
    r1 = fields.Int(required=True, attribute='result_field1', data_key='X')
    r2 = fields.List(fields.Int(), required=True,
                     attribute='result_field2', data_key='Y')
    nested = fields.XMLNested(ComplicatedXMLNested2, many=True,
                              attribute='result_field3', data_key='Z')


class ComplicatedXML(XMLSchema):
    root = fields.XMLNested(ComplicatedXMLNested, required=True)

    @post_load
    def data_from_root(self, item):
        return item[self.fields['root'].name]
