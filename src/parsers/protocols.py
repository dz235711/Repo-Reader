from typing import Protocol, TypeVar

from core.models import ParsedFile, ParserContext

_Context = TypeVar("_Context", bound=ParserContext, contravariant=True)


class Parser(Protocol):
    def parse(self, code: bytes, context: _Context) -> ParsedFile: ...
