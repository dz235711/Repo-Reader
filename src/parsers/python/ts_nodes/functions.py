from enum import StrEnum, IntEnum

from .core import Fields, NameTypes

TYPE_PARAMETER_NODE_WRAPPER = "type"
PARAMETER_NODE_WRAPPER = "parameter"


class FunctionNodeType(StrEnum):
    FUNCTION_DEFINITION = "function_definition"
    DECORATED_DEFINITION = "decorated_definition"


class FunctionDefinitionFields(StrEnum):
    NAME = Fields.NAME
    TYPE_PARAMETERS = "type_parameters"
    PARAMETERS = "parameters"
    RETURN_TYPE = "return_type"


class FunctionDefinitionNodeTypes(StrEnum):
    ASYNC = "async"


class TypeParameterChildrenTypes(StrEnum):
    IDENTIFIER = NameTypes.IDENTIFIER
    CONSTRAINED_TYPE = "constrained_type"
    SPLAT_TYPE = "splat_type"


class ConstrainedTypeParameterChildrenIndices(IntEnum):
    NAME = 0
    CONSTRAINTS = 2


class SplatTypeParameterPrefixes(StrEnum):
    TUPLE = "*"
    SPEC = "**"


class SplatTypeParameterChildrenIndices(IntEnum):
    PREFIX = 0
    NAME = 1


class ParameterChildrenTypes(StrEnum):
    TYPED_PARAMETER = "typed_parameter"
    POSITIONAL_SEPARATOR = "positional_separator"
    TYPED_DEFAULT_PARAMETER = "typed_default_parameter"
    IDENTIFIER = NameTypes.IDENTIFIER
    KEYWORD_SEPARATOR = "keyword_separator"
    LIST_SPLAT = "list_splat_pattern"
    DICT_SPLAT = "dictionary_splat_pattern"


class TypedParameterChildrenIndices(IntEnum):
    VARIANT = 0
    TYPE = 2


class TypedParameterNameTypes(StrEnum):
    IDENTIFIER = NameTypes.IDENTIFIER
    LIST_SPLAT = "list_splat_pattern"
    DICT_SPLAT = "dictionary_splat_pattern"


class TypedDefaultParameterFields(StrEnum):
    NAME = "name"
    TYPE = "type"
    VALUE = "value"


class DecoratedDefinitionTypes(StrEnum):
    DECORATOR = "decorator"
    DEFINITION = FunctionNodeType.FUNCTION_DEFINITION
