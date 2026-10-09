from dataclasses import dataclass
from pathlib import Path

import tree_sitter_python as tspython
import tree_sitter as ts

from configs.languages import Language

from .ts_nodes.imports import ImportNodeTypes
from .ts_nodes.functions import FunctionNodeTypes
from .subparsers.imports import parse_import
from .subparsers.functions import parse_function
from .model.functions import Function
from .model.imports import Import
from core.models import ParsedFile, ParserContext


class Parser:
    __slots__ = ["_parser"]

    @dataclass(frozen=True, slots=True, kw_only=True)
    class ParsedFile(ParsedFile):
        imports: tuple[Import, ...] = ()
        functions: tuple[Function, ...] = ()

    @dataclass(frozen=True, slots=True, kw_only=True)
    class ParserContext(ParserContext):
        import_root: Path | None = None

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, code: bytes, context: Parser.ParserContext) -> Parser.ParsedFile:
        tree = self._parser.parse(code)

        imports = []
        functions = []

        fringe = [tree.root_node]
        while fringe:
            node = fringe.pop()
            if node.type in ImportNodeTypes:
                imports.append(parse_import(node))
            elif node.type in FunctionNodeTypes:
                functions.append(parse_function(node))
            else:
                fringe.extend(node.children)

        return Parser.ParsedFile(
            rel_path=context.rel_path,
            language=Language.PYTHON,
            imports=tuple(imports),
            functions=tuple(functions),
        )
