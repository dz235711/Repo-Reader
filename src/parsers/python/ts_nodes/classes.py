from enum import StrEnum, IntEnum

from .core import Fields


class ClassNodeTypes(StrEnum):
    CLASS_DEFINITION = "class_definition"


class ClassDefinitionFields(StrEnum):
    NAME = Fields.NAME
    BASE_CLASSES = "base_classes"
    BODY = "body"
