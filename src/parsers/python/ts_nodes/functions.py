from enum import StrEnum, IntEnum

from .core import Fields

TYPE_PARAMETER_NODE_TYPE = "type"
TUPLE = "tuple"


class FunctionNodeType(StrEnum):
    FUNCTION_DEFINITION = "function_definition"


class FunctionDefinitionFields(StrEnum):
    NAME = Fields.NAME
    TYPE_PARAMETERS = "type_parameters"


class FunctionDefinitionNodeTypes(StrEnum):
    ASYNC = "async"


class TypeParameterChildrenTypes(StrEnum):
    IDENTIFIER = "identifier"
    CONSTRAINED_TYPE = "constrained_type"
    SPLAT_TYPE = "splat_type"


class ConstrainedTypeParameterChildrenIndices(IntEnum):
    NAME = 0
    CONSTRAINTS = 2


class SplatTypeParameterPrefixes(StrEnum):
    STAR = "*"
    DOUBLE_STAR = "**"


class SplatTypeParameterChildrenIndices(IntEnum):
    PREFIX = 0
    NAME = 1
