from enum import Enum


class OPERATOR_MONGODB(Enum):
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
