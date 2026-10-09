from dataclasses import dataclass
from typing import TYPE_CHECKING


from core.models import Body as GenericBody
from . import functions as functions_model
from . import imports as imports_model
from . import classes as classes_model


@dataclass(frozen=True, slots=True, kw_only=True)
class Body(GenericBody):
    imports: tuple[imports_model.Import, ...] = ()
    functions: tuple[functions_model.Function, ...] = ()
    classes: tuple[classes_model.Class, ...] = ()
