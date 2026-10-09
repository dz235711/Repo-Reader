from dataclasses import dataclass
from pathlib import Path

import tree_sitter_python as tspython
import tree_sitter as ts

from configs.languages import Language

from .subparsers.body import parse_body
from core.models import ParsedFile, ParserContext


class Parser:
    __slots__ = ["_parser"]

    @dataclass(frozen=True, slots=True, kw_only=True)
    class ParserContext(ParserContext):
        import_root: Path | None = None

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, code: bytes, context: Parser.ParserContext) -> ParsedFile:
        tree = self._parser.parse(code)

        return ParsedFile(
            rel_path=context.rel_path,
            language=Language.PYTHON,
            body=parse_body(tree.root_node),
        )
