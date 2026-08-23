import tree_sitter as ts

from core.models import SourceSpan, Coordinate

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


def child_of(node: ts.Node, name: str) -> ts.Node:
    child = node.child_by_field_name(name)
    assert child is not None
    return child


def first_type_of(node: ts.Node, type: str) -> ts.Node:
    for child in node.children:
        if child.type == type:
            return child
    assert False


def decode(bytes: bytes) -> str:
    return bytes.decode(_TS_ENCODING)
