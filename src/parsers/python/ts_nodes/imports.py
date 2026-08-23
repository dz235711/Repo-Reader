from enum import StrEnum

from .core import Fields, NameTypes


class ImportNodeType(StrEnum):
    IMPORT_STATEMENT = "import_statement"
    FUTURE_IMPORT_STATEMENT = "future_import_statement"
    IMPORT_FROM_STATEMENT = "import_from_statement"


class ImportStatementFields(StrEnum):
    NAME = Fields.NAME


class ImportNameTypes(StrEnum):
    ALIASED_IMPORT = "aliased_import"
    DOTTED_NAME = NameTypes.DOTTED_NAME


class AliasedImportFields(StrEnum):
    NAME = Fields.NAME
    ALIAS = "alias"


class ImportFromFields(StrEnum):
    MODULE_NAME = "module_name"
    NAME = Fields.NAME


class ImportFromTypes(StrEnum):
    WILDCARD_IMPORT = "wildcard_import"


class ModuleNameTypes(StrEnum):
    DOTTED_NAME = NameTypes.DOTTED_NAME
    RELATIVE_IMPORT = "relative_import"


class RelativeImportChildTypes(StrEnum):
    DOTTED_NAME = NameTypes.DOTTED_NAME
    IMPORT_PREFIX = "import_prefix"
