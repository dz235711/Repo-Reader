from dataclasses import dataclass, field

from core.models import SourceSpan, Expression


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
class Parameter:
    name: Expression
    span: SourceSpan
    annotation: Expression | None = None
    default_value: Expression | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Parameters:
    regulars: tuple[Parameter, ...] = ()
    positionals: tuple[Parameter, ...] = ()
    keywords: tuple[Parameter, ...] = ()
    var_positional: Parameter | None = None
    var_keyword: Parameter | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class PositionalArgument:
    value: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class KeywordArgument(PositionalArgument):
    name: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class Arguments:
    positional_argument: tuple[PositionalArgument, ...] = ()
    keyword_arguments: tuple[KeywordArgument, ...] = ()
    iterable_unpacking: tuple[PositionalArgument, ...] = ()
    keyword_unpacking: tuple[PositionalArgument, ...] = ()


@dataclass(frozen=True, slots=True, kw_only=True)
class Decorator:
    # TODO: its any arbitrary expression that evaluates to the decorator signature
    # parse after body_span for Function is expanded on
    body: Expression


@dataclass(frozen=True, slots=True, kw_only=True)
class Function:
    name: Expression
    span: SourceSpan
    body_span: SourceSpan  # TODO: parse further once initial works
    is_async: bool = False
    type_parameters: TypeParameters = field(default_factory=TypeParameters)
    parameters: Parameters = field(default_factory=Parameters)
    return_annotation: Expression | None = None
    decorators: tuple[Decorator, ...] = ()
    is_method: bool = False
    parent: Function | None = None  # TODO: also class once that is added
