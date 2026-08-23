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


def types_of(
    node: ts.Node, types: set[str], per_type_cap: int = 0
) -> dict[str, list[ts.Node]]:
    matched = dict()
    filled = 0
    for child in node.children:
        if child.type in types:
            matched_nodes = matched.setdefault(child.type, [])
            if per_type_cap <= 0 or len(matched_nodes) < per_type_cap:
                matched_nodes.append(child)
                if per_type_cap > 0 and len(matched_nodes) == per_type_cap:
                    filled += 1
                    if filled == len(types):
                        break
    return matched


def only_types_of(node: ts.Node, types: set[str]) -> dict[str, ts.Node]:
    matched = types_of(node, types)
    assert all(len(nodes) == 1 for nodes in matched.values())
    return {type: nodes[0] for type, nodes in matched.items()}


def only_type_of(node: ts.Node, type: str) -> ts.Node:
    return only_types_of(node, {type})[type]


def first_types_of(node: ts.Node, types: set[str]) -> dict[str, ts.Node]:
    matched = types_of(node, types, per_type_cap=1)
    return {type: nodes[0] for type, nodes in matched.items()}


def first_type_of(node: ts.Node, type: str) -> ts.Node:
    return first_types_of(node, {type})[type]


def decode(bytes: bytes) -> str:
    return bytes.decode(_TS_ENCODING)
