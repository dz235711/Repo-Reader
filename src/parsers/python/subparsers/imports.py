from dataclasses import replace

import tree_sitter as ts

from core.models import Expression
from core.utils import flatten, map_t
from adaptors.treesitter import (
    span_from_node,
    child_of,
    decode,
    only_type_of,
    only_types_of,
    types_of,
)

from .core import parse_name
from ..model.imports import (
    ImportStatement,
    ImportName,
    FutureImportStatement,
    ImportFromStatement,
    WildCardImport,
    RelativeImport,
    Import,
)
from ..ts_nodes.imports import (
    ImportNodeTypes,
    AliasedImportFields,
    ImportFromFields,
    ImportFromTypes,
    ModuleNameTypes,
    RelativeImportChildTypes,
    ImportStatementFields,
    ImportNameTypes,
)
from ..ts_nodes.core import NameTypes


def parse_import(node: ts.Node) -> Import:
    match ImportNodeTypes(node.type):
        case ImportNodeTypes.IMPORT_FROM_STATEMENT:
            return _parse_import_from_statement(node)
        case ImportNodeTypes.FUTURE_IMPORT_STATEMENT:
            return _parse_future_import_statement(node)
        case ImportNodeTypes.IMPORT_STATEMENT:
            return _parse_import_statement(node)


def _parse_import_name(node: ts.Node) -> ImportName:
    match ImportNameTypes(node.type):
        case ImportNameTypes.ALIASED_IMPORT:
            alias = child_of(node, AliasedImportFields.ALIAS)
            return replace(
                _parse_import_name(child_of(node, AliasedImportFields.NAME)),
                span=span_from_node(node),
                alias=parse_name(alias),
            )
        case ImportNameTypes.DOTTED_NAME:
            return ImportName(
                name=parse_name(node),
                span=span_from_node(node),
            )


def _parse_import_statement(node: ts.Node) -> ImportStatement:
    span = span_from_node(node)
    names = map_t(
        _parse_import_name,
        node.children_by_field_name(ImportStatementFields.NAME),
    )
    return ImportStatement(names=names, span=span)


def _parse_future_import_statement(node: ts.Node) -> FutureImportStatement:
    span = span_from_node(node)
    names = map_t(
        _parse_import_name,
        flatten(types_of(node, set(ImportNameTypes)).values(), (ts.Node,)),
    )
    return FutureImportStatement(names=names, span=span)


def _parse_module_name(node: ts.Node) -> Expression | RelativeImport:
    match ModuleNameTypes(node.type):
        case ModuleNameTypes.DOTTED_NAME:
            return parse_name(node)
        case ModuleNameTypes.RELATIVE_IMPORT:
            matched = only_types_of(node, set(RelativeImportChildTypes))
            prefix = matched[RelativeImportChildTypes.IMPORT_PREFIX]
            level = prefix.end_point.column - prefix.start_point.column
            name = matched.get(RelativeImportChildTypes.DOTTED_NAME)
            return RelativeImport(
                relative_level=level,
                module_name=parse_name(name).name if name is not None else None,
                span=span_from_node(node),
            )


def _parse_import_from_statement(node: ts.Node) -> ImportFromStatement:
    span = span_from_node(node)
    module_node = _parse_module_name(child_of(node, ImportFromFields.MODULE_NAME))
    members = map_t(
        _parse_import_name,
        node.children_by_field_name(ImportFromFields.NAME),
    )
    if not members:
        wildcard = only_type_of(node, ImportFromTypes.WILDCARD_IMPORT)
        members = WildCardImport(span=span_from_node(wildcard))
    return ImportFromStatement(
        members=members,
        span=span,
        module=module_node,
    )
