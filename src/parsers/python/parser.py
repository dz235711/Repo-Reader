import tree_sitter_python as tspython
import tree_sitter as ts

from configs.languages import Language

from .model.core import PythonParsedFile, PythonParserContext
from .ts_nodes.imports import ImportNodeType

from .extractors.imports import (
    parse_import_statement,
)


class Parser:
    __slots__ = ["_parser"]

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, code: bytes, context: PythonParserContext) -> PythonParsedFile:
        tree = self._parser.parse(code)

        imports = []

        fringe = [tree.root_node]
        while fringe:
            node = fringe.pop()
            match node.type:
                case ImportNodeType():
                    imports.append(parse_import_statement(node))
                case _:
                    fringe.extend(node.children)

        return PythonParsedFile(
            rel_path=context.rel_path,
            language=Language.PYTHON,
            imports=tuple(imports),
        )
