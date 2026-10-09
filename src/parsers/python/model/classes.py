from dataclasses import dataclass, field

from core.models import SourceSpan, Expression

from .core import TypeParameters, Decorator, Argument, Scope
from . import body as body_model


@dataclass(frozen=True, slots=True, kw_only=True)
class Class(Scope):
    name: Expression
    span: SourceSpan
    body: body_model.Body
    type_parameters: TypeParameters = field(default_factory=TypeParameters)
    arguments: tuple[Argument, ...] = ()
    decorators: tuple[Decorator, ...] = ()
    parent: Scope | None = None
