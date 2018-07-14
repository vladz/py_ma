from marshmallow import utils
from marshmallow.fields import *


class XMLNested(Nested):
    def _deserialize(self, value, attr, data):
        if self.many and not utils.is_collection(value):
            value = [value]
        return super()._deserialize(value, attr, data)
