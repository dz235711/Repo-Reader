from dataclasses import dataclass

from core.models import SourceSpan, Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class Parameter:
    name: Expression
    span: SourceSpan
    annotation: Expression | None
    default_value: Expression | None


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
    regulars: tuple[TypeParameter, ...]
    tuples: tuple[PlainTypeParameter, ...]
    specs: tuple[PlainTypeParameter, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class Parameters:
    parameters: tuple[Parameter, ...]
    positional_parameters: tuple[Parameter, ...]
    keyword_parameters: tuple[Parameter, ...]
    var_positional_parameter: Parameter | None
    var_keyword_parameter: Parameter | None


@dataclass(frozen=True, slots=True, kw_only=True)
class PositionalArgument:
    value: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class KeywordArgument(PositionalArgument):
    name: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class Arguments:
    positional_argument: tuple[PositionalArgument, ...]
    keyword_arguments: tuple[KeywordArgument, ...]
    iterable_unpacking: tuple[PositionalArgument, ...]
    keyword_unpacking: tuple[PositionalArgument, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class Decorator:
    name: Expression
    arguments: Arguments


@dataclass(frozen=True, slots=True, kw_only=True)
class Function:
    name: Expression
    qualified_name: str | None
    span: SourceSpan
    is_async: bool
    type_parameters: TypeParameters
    parameters: Parameters
    decorators: tuple[Decorator, ...]
    body_span: SourceSpan  # TODO: parse further once initial works
    return_annotation: Expression
    is_method: bool
    parent_qualified_name: str | None = None
