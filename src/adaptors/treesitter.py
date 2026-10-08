import tree_sitter as ts
from collections.abc import Callable, Generator

from core.models import SourceSpan, Coordinate, Expression

_TS_ENCODING = "utf-8"


def span_from_node(node: ts.Node) -> SourceSpan:
    return SourceSpan(
        start=Coordinate(
            line=node.start_point.row,
            column=node.start_point.column,
            byte_offset=node.start_byte,
        ),
        end=Coordinate(
            line=node.end_point.row,
            column=node.end_point.column,
            byte_offset=node.end_byte,
        ),
    )


def expression_from_node(node: ts.Node) -> Expression:
    assert node.text is not None
    return Expression(
        name=decode(node.text),
        span=span_from_node(node),
    )


def child_of(node: ts.Node, name: str) -> ts.Node:
    child = node.child_by_field_name(name)
    assert child is not None
    return child


def only_child_of(node: ts.Node) -> ts.Node:
    assert len(node.children) == 1
    return node.children[0]


def types_of(node: ts.Node, types: set[str]) -> Generator[ts.Node, None, None]:
    for child in node.children:
        if child.type in types:
            yield child


def only_type_of(node: ts.Node, types: str) -> ts.Node:
    matcheds = types_of(node, {types})
    matched = next(matcheds, None)
    assert matched is not None and next(matcheds, None) is None
    return matched


def has_type_of(node: ts.Node, types: set[str]) -> bool:
    matcheds = types_of(node, types)
    return next(matcheds, None) is not None


def exec_if_named_child[T](
    func: Callable[[ts.Node], T], node: ts.Node, name: str, default: Callable[[], T]
) -> T:
    child = node.child_by_field_name(name)
    return func(child) if child is not None else default()


def named_child_of(node: ts.Node, name: str) -> ts.Node:
    child = node.child_by_field_name(name)
    assert child is not None
    return child


def decode(bytes: bytes) -> str:
    return bytes.decode(_TS_ENCODING)
