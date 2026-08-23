import tree_sitter_python as tspython
import tree_sitter as ts

from configs.languages import Language

from .model.core import PythonParsedFile, PythonParserContext
from .ts_nodes.imports import ImportNodeTypes
from .ts_nodes.functions import FunctionNodeType
from .subparsers.imports import parse_import
from .subparsers.functions import parse_function


class Parser:
    __slots__ = ["_parser"]

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, code: bytes, context: PythonParserContext) -> PythonParsedFile:
        tree = self._parser.parse(code)

        imports = []
        functions = []

        fringe = [tree.root_node]
        while fringe:
            node = fringe.pop()
            if node.type in ImportNodeTypes:
                imports.append(parse_import(node))
            elif node.type in FunctionNodeType:
                functions.append(parse_function(node))
            else:
                fringe.extend(node.children)

        return PythonParsedFile(
            rel_path=context.rel_path,
            language=Language.PYTHON,
            imports=tuple(imports),
        )
