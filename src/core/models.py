from dataclasses import dataclass
from pathlib import Path

from configs.languages import Language


@dataclass(frozen=True, slots=True, kw_only=True)
class ParsedFile:
    rel_path: Path
    language: Language


@dataclass(frozen=True, slots=True, kw_only=True)
class Coordinate:
    line: int
    column: int
    byte_offset: int


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceSpan:
    start: Coordinate
    end: Coordinate


@dataclass(frozen=True, slots=True, kw_only=True)
class Expression:
    name: str
    span: SourceSpan


@dataclass(frozen=True, slots=True, kw_only=True)
class ParserContext:
    rel_path: Path
