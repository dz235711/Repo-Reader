from dataclasses import dataclass

from core.models import SourceSpan, Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class ImportName:
    name: Expression
    span: SourceSpan
    alias: Expression | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ImportStatement:
    names: tuple[ImportName, ...]
    span: SourceSpan
    scope_qualified_name: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class FutureImportStatement:
    names: tuple[ImportName, ...]
    span: SourceSpan


@dataclass(frozen=True, slots=True, kw_only=True)
class WildCardImport:
    span: SourceSpan


@dataclass(frozen=True, slots=True, kw_only=True)
class RelativeImport:
    relative_level: int
    span: SourceSpan
    module_name: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ImportFromStatement:
    members: tuple[ImportName, ...] | WildCardImport
    span: SourceSpan
    module: Expression | RelativeImport
    scope_qualified_name: str | None = None


type Import = ImportStatement | FutureImportStatement | ImportFromStatement
