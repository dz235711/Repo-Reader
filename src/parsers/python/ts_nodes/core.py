from enum import StrEnum


class Fields(StrEnum):
    NAME = "name"


class NameTypes(StrEnum):
    DOTTED_NAME = "dotted_name"
    NAME = "name"
    IDENTIFIER = "identifier"


class CollectionTypes(StrEnum):
    TUPLE = "tuple"
