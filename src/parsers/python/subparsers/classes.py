import tree_sitter as ts

from adaptors.treesitter import (
    named_child_of,
    expression_from_node,
    span_from_node,
)

from ..ts_nodes.classes import ClassNodeTypes, ClassDefinitionFields
from ..model.classes import Class
from ..subparsers import body as body_parser


def parse_class(node: ts.Node) -> Class:
    match ClassNodeTypes(node.type):
        case ClassNodeTypes.CLASS_DEFINITION:
            name = expression_from_node(
                named_child_of(node, ClassDefinitionFields.NAME)
            )
            body = body_parser.parse_body(
                named_child_of(node, ClassDefinitionFields.BODY)
            )
            return Class(name=name, span=span_from_node(node), body=body)
