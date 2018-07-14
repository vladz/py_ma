import csv
import io
from typing import Dict

from marshmallow import Schema, SchemaOpts
import xmltodict


class CSVOptions(SchemaOpts):
    def __init__(self, meta, ordered=True):
        super().__init__(meta, ordered)
        self.dateformat = 'iso'
        self.render_module = csv
        # self.ordered = True


class CSVSchema(Schema):
    OPTIONS_CLASS = CSVOptions

    def loads(self, csv_data: str, many: bool = None, *args, **kwargs) -> Dict:
        partial = kwargs.pop('partial', None)
        f = io.StringIO(csv_data)
        data = self.opts.render_module.DictReader(f)
        data = list(data)
        if len(data) == 1 and not many:
            data = data[0]
        return self.load(data, many=many, partial=partial)


class XMLOptions(SchemaOpts):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dateformat = 'iso'
        self.render_module = xmltodict
        # self.ordered = True


class XMLSchema(Schema):
    OPTIONS_CLASS = XMLOptions

    def loads(self, csv_data: str, many: bool = None, *args, **kwargs) -> Dict:
        partial = kwargs.pop('partial', None)
        data = self.opts.render_module.parse(csv_data)
        return self.load(data, many=many, partial=partial)


class JSONOptions(SchemaOpts):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dateformat = 'iso'
        # self.ordered = True


class JSONSchema(Schema):
    OPTIONS_CLASS = JSONOptions
