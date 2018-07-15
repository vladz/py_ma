import csv
import io

from marshmallow import Schema, SchemaOpts
import xmltodict


class CSVOptions(SchemaOpts):
    def __init__(self, meta, ordered=True):
        super().__init__(meta, ordered)
        self.dateformat = 'iso'
        self.render_module = csv


class CSVSchema(Schema):
    OPTIONS_CLASS = CSVOptions

    def loads(self, csv_data: str, many: bool = None, *args, **kwargs):
        partial = kwargs.pop('partial', None)
        buf = io.StringIO(csv_data)
        data = self.opts.render_module.DictReader(buf)
        data = list(data)
        if len(data) == 1 and not many:
            data = data[0]
        return self.load(data, many=many, partial=partial)


class XMLOptions(SchemaOpts):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dateformat = 'iso'
        self.render_module = xmltodict


class XMLSchema(Schema):
    OPTIONS_CLASS = XMLOptions

    def loads(self, xml_data: str, many: bool = None, *args, **kwargs):
        partial = kwargs.pop('partial', None)
        data = self.opts.render_module.parse(xml_data)
        return self.load(data, many=many, partial=partial)


class JSONOptions(SchemaOpts):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dateformat = 'iso'


class JSONSchema(Schema):
    OPTIONS_CLASS = JSONOptions
