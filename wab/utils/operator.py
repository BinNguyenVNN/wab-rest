from enum import Enum


class OperatorMongo(Enum):
    operator_in = ('in', 'in')
    operator_not_in = ('not_in', 'not in')
    operator_contains = ('contains', 'regex')
    operator_equals = ('equals', '=')
    operator_not_equals = ('not_equals', '!=')
    operator_less_than = ('less_than', '<')
    operator_less_than_or_equals = ('less_than_or_equals', '<=')
    operator_greater_than = ('greater_than', '>')
    operator_greater_than_or_equals = ('less_greater_than_or_equals', '>=')

    # operator_range = ('range', 'range')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class MergeType(Enum):
    inner_join = ('inner join', 'inner join')
    left_join = ('left join', 'left join')
    right_join = ('right join', 'right join')
    right_outer_join = ('right outer join', 'right outer join')
    union = ('union', 'union')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class Relation(Enum):
    relation_and = ('and', 'and')
    relation_or = ('or', 'or')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class MongoColumnType(Enum):
    double = (1, 'double')
    string = (2, 'string')
    object = (3, 'object')
    array = (4, 'array')
    binData = (5, 'binData')
    undefined = (6, 'undefined')
    objectId = (7, 'objectId')
    bool = (8, 'bool')
    date = (9, 'date')
    null = (10, 'null')
    regex = (11, 'regex')
    dbPointer = (12, 'dbPointer')
    javascript = (13, 'javascript')
    symbol = (14, 'symbol')
    javascriptWithScope = (15, 'javascriptWithScope')
    int = (16, 'int')
    timestamp = (17, 'timestamp')
    long = (18, 'long')
    decimal = (19, 'decimal')
    minKey = (-1, 'minKey')
    maxKey = (127, 'maxKey')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def get_name(cls, member):
        return cls[member].value[1]

    @classmethod
    def get_type(cls, member):
        return cls[member].value[0], cls[member].value[1]


class RegexType(Enum):
    IS_NUMBER = ('is_number', 'Is Number')
    IS_TEXT_ONLY = ('is_text_only', 'Is Text Only')
    IS_EMAIL = ('is_email', 'Is Email')
    IS_PHONE = ('is_phone', 'Is Phone')
    IS_CUSTOM = ('is_custom', 'Is Custom')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def get_name(cls, member):
        return cls[member].value[1]

    @classmethod
    def get_type(cls, member):
        return cls[member].value[0], cls[member].value[1]
