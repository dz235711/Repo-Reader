import tree_sitter as ts

from adaptors.treesitter import span_from_node

from ..model.body import Body
from . import imports as imports_parser
from . import functions as functions_parser
from . import classes as classes_parser
from ..ts_nodes.imports import ImportNodeTypes
from ..ts_nodes.functions import FunctionNodeTypes
from ..ts_nodes.classes import ClassNodeTypes


def parse_body(node: ts.Node) -> Body:
    imports = []
    functions = []
    classes = []

    fringe = [node]
    while fringe:
        cur_node = fringe.pop()
        if cur_node.type in ImportNodeTypes:
            imports.append(imports_parser.parse_import(cur_node))
        elif cur_node.type in FunctionNodeTypes:
            functions.append(functions_parser.parse_function(cur_node))
        elif cur_node.type in ClassNodeTypes:
            classes.append(classes_parser.parse_class(cur_node))
        else:
            fringe.extend(cur_node.children)

    return Body(
        span=span_from_node(node),
        imports=tuple(imports),
        functions=tuple(functions),
        classes=tuple(classes),
    )
