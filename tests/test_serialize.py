import pytest

from tests import samples


class TestSchemas:
    @pytest.mark.parametrize('schema_class, data, expected', [
        (samples.SimpleJSON, samples.simple_json, samples.simple_dict),
        (samples.SimpleXML, samples.simple_xml, samples.simple_dict),
        (samples.SimpleCSV, samples.simple_csv, samples.simple_dict),
    ])
    def test_simple_json(self, schema_class, data, expected):
        schema = schema_class()
        result = schema.loads(data)
        assert expected == result


class TestComplicatedchemas:
    @pytest.mark.parametrize('schema_class, data, expected', [
        (samples.ComplicatedJSON, samples.complicated_json,
         samples.complicated_dict),
        (samples.ComplicatedXML, samples.complicated_xml,
         samples.complicated_dict),
    ])
    def test_complicated(self, schema_class, data, expected):
        schema = schema_class()
        result = schema.loads(data)
        assert expected == result
