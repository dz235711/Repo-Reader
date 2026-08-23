from dataclasses import replace

import tree_sitter as ts

from core.models import Expression

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
    ImportNodeType,
    ImportNameTypes,
    AliasedImportFields,
    ImportFromFields,
    ImportFromTypes,
    NameTypes,
    ModuleNameTypes,
    RelativeImportChildTypes,
    ImportStatementFields,
)
from adaptors.treesitter import span_from_node, child_of, decode, first_type_of


def parse_import(node: ts.Node) -> Import:
    match ImportNodeType(node.type):
        case ImportNodeType.IMPORT_FROM_STATEMENT:
            return parse_import_from_statement(node)
        case ImportNodeType.FUTURE_IMPORT_STATEMENT:
            return parse_future_import_statement(node)
        case ImportNodeType.IMPORT_STATEMENT:
            return parse_import_statement(node)


def parse_name(node: ts.Node) -> Expression:
    match NameTypes(node.type):
        case NameTypes.DOTTED_NAME | NameTypes.NAME:
            assert node.text is not None
            return Expression(name=decode(node.text), span=span_from_node(node))


def parse_import_name(node: ts.Node) -> ImportName:
    match ImportNameTypes(node.type):
        case ImportNameTypes.ALIASED_IMPORT:
            import_name = parse_import_name(child_of(node, AliasedImportFields.NAME))
            alias = child_of(node, AliasedImportFields.ALIAS)
            assert alias.text is not None
            return replace(
                import_name,
                span=span_from_node(node),
                alias=Expression(name=decode(alias.text), span=span_from_node(alias)),
            )
        case ImportNameTypes.DOTTED_NAME:
            return ImportName(
                name=parse_name(node),
                span=span_from_node(node),
            )


def parse_import_statement(node: ts.Node) -> ImportStatement:
    span = span_from_node(node)
    names = tuple(
        parse_import_name(child)
        for child in node.children_by_field_name(ImportStatementFields.NAME)
    )
    return ImportStatement(names=names, span=span, scope_qualified_name=None)


def parse_future_import_statement(node: ts.Node) -> FutureImportStatement:
    span = span_from_node(node)
    names = tuple(
        parse_import_name(child)
        for child in node.children
        if child.type in ImportNameTypes
    )
    return FutureImportStatement(names=names, span=span)


def parse_module_name(node: ts.Node) -> Expression | RelativeImport:
    match ModuleNameTypes(node.type):
        case ModuleNameTypes.DOTTED_NAME:
            return parse_name(node)
        case ModuleNameTypes.RELATIVE_IMPORT:
            level = None
            name = None
            for child in node.children:
                match RelativeImportChildTypes(child.type):
                    case RelativeImportChildTypes.IMPORT_PREFIX:
                        level = child.end_point.column - child.start_point.column
                    case RelativeImportChildTypes.DOTTED_NAME:
                        name = parse_name(child).name
            assert level is not None
            return RelativeImport(
                relative_level=level,
                module_name=name,
                span=span_from_node(node),
            )


def parse_import_from_statement(node: ts.Node) -> ImportFromStatement:
    span = span_from_node(node)
    module_node = parse_module_name(child_of(node, ImportFromFields.MODULE_NAME))
    members = tuple(
        parse_import_name(child)
        for child in node.children_by_field_name(ImportFromFields.NAME)
    )
    if not members:
        wildcard = first_type_of(node, ImportFromTypes.WILDCARD_IMPORT)
        members = WildCardImport(span=span_from_node(wildcard))
    return ImportFromStatement(
        members=members,
        span=span,
        module=module_node,
        scope_qualified_name=None,
    )
