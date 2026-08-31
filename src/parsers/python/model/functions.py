from dataclasses import dataclass, field

from core.models import SourceSpan, Expression

from .core import TypeParameters, Decorator, Scope


@dataclass(frozen=True, slots=True, kw_only=True)
class Parameter:
    index: int
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
class Function(Scope):
    name: Expression
    span: SourceSpan
    body_span: SourceSpan  # TODO: parse further once initial works
    is_async: bool = False
    type_parameters: TypeParameters = field(default_factory=TypeParameters)
    parameters: Parameters = field(default_factory=Parameters)
    return_annotation: Expression | None = None
    decorators: tuple[Decorator, ...] = ()
    parent: Scope | None = None
