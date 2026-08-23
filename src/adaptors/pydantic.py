from typing import TypeVar, Annotated, Any, get_args, Mapping

from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    chain_schema,
    no_info_plain_validator_function,
    json_or_python_schema,
    plain_serializer_function_ser_schema,
)
from pydantic import GetCoreSchemaHandler
from frozendict import frozendict


class _PydanticFrozenDictAnnotation:

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        key_type, value_type = get_args(source_type)

        def freeze(
            mapping: Mapping[key_type, value_type],
        ) -> frozendict[key_type, value_type]:
            return frozendict(mapping)

        frozendict_schema = chain_schema(
            [
                handler.generate_schema(dict[key_type, value_type]),
                no_info_plain_validator_function(freeze),
            ]
        )
        return json_or_python_schema(
            json_schema=frozendict_schema,
            python_schema=frozendict_schema,
            serialization=plain_serializer_function_ser_schema(dict),
        )


_K = TypeVar("_K")
_V = TypeVar("_V")
FrozenDict = Annotated[frozendict[_K, _V], _PydanticFrozenDictAnnotation]
