from dataclasses import dataclass
from pathlib import Path

from core.models import ParsedFile, ParserContext

from .imports import Import


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonParsedFile(ParsedFile):
    imports: tuple[Import, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonParserContext(ParserContext):
    import_root: Path | None = None
