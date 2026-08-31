from dataclasses import dataclass
from pathlib import Path

from core.models import ParsedFile, ParserContext, Expression, SourceSpan

from .imports import Import


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonParsedFile(ParsedFile):
    imports: tuple[Import, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonParserContext(ParserContext):
    import_root: Path | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class _TypeParameter:
    name: Expression
    default: Expression | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class PlainTypeParameter(_TypeParameter):
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class BoundTypeParameter(_TypeParameter):
    bind: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class ConstrainedTypeParameter(_TypeParameter):
    constraints: tuple[Expression, ...]


type TypeParameter = PlainTypeParameter | BoundTypeParameter | ConstrainedTypeParameter


@dataclass(frozen=True, slots=True, kw_only=True)
class TypeParameters:
    regulars: tuple[TypeParameter, ...] = ()
    tuples: tuple[PlainTypeParameter, ...] = ()
    specs: tuple[PlainTypeParameter, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class Decorator:
    # TODO: its any arbitrary expression that evaluates to the decorator signature
    # parse after body_span for Function is expanded on
    body: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class _Argument:
    index: int
    value: Expression
    span: SourceSpan


@dataclass(frozen=True, slots=True, kw_only=True)
class PlainArgument(_Argument):
    name: Expression | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class UnpackingArgument(_Argument):
    is_keyword: bool


type Argument = PlainArgument | UnpackingArgument


@dataclass(frozen=True, slots=True, kw_only=True)
class Scope:
    pass
