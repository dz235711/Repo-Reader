import tree_sitter as ts

from adaptors.treesitter import expression_from_node
from core.models import Expression

from ..ts_nodes.core import NameTypes


def parse_name(node: ts.Node) -> Expression:
    match NameTypes(node.type):
        case NameTypes.DOTTED_NAME | NameTypes.NAME | NameTypes.IDENTIFIER:
            return expression_from_node(node)
