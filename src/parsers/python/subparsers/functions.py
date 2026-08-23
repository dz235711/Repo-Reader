import tree_sitter as ts

from adaptors.treesitter import (
    span_from_node,
    named_child_of,
    expression_from_node,
    type_of,
    types_of,
    only_child_of,
)
from core.utils import map_t, flatten

from ..ts_nodes.functions import (
    FunctionNodeType,
    FunctionDefinitionFields,
    FunctionDefinitionNodeTypes,
    TypeParameterChildrenTypes,
    TYPE_PARAMETER_NODE_TYPE,
    ConstrainedTypeParameterChildrenIndices,
    TUPLE,
)
from ..model.functions import (
    Function,
    TypeParameter,
    TypeParameters,
    GenericTypeParameter,
    ConstrainedTypeParameters,
    BoundedTypeParameter,
)


def parse_function(node: ts.Node) -> Function:
    match FunctionNodeType(node.type):
        case FunctionNodeType.FUNCTION_DEFINITION:
            name = expression_from_node(
                named_child_of(node, FunctionDefinitionFields.NAME)
            )
            type_parameters = _parse_type_parameters(
                named_child_of(node, FunctionDefinitionFields.TYPE_PARAMETERS)
            )
            matched = types_of(node, set(FunctionDefinitionNodeTypes))
            # return Function(
            #     name=name,
            #     qualified_name=None,
            #     span=span_from_node(node),
            #     is_async=FunctionDefinitionNodeTypes.ASYNC in matched,
            # )


def _parse_type_parameters(node: ts.Node) -> TypeParameters:
    map_t(
        _parse_type_parameter,
        map(only_child_of, type_of(node, TYPE_PARAMETER_NODE_TYPE)),
    )


def _parse_type_parameter(node: ts.Node) -> TypeParameter:
    # NOTE: current python treesitter grammar is 3.12 so defaults can't be parsed
    match TypeParameterChildrenTypes(node.type):
        case TypeParameterChildrenTypes.IDENTIFIER:
            return GenericTypeParameter(
                name=expression_from_node(node),
            )
        case TypeParameterChildrenTypes.CONSTRAINED_TYPE:
            name_node = only_child_of(
                node.children[ConstrainedTypeParameterChildrenIndices.NAME]
            )
            constraint_node = only_child_of(
                node.children[ConstrainedTypeParameterChildrenIndices.CONSTRAINTS]
            )
            name = expression_from_node(name_node)
            constraints = (
                type_of(constraint_node, TypeParameterChildrenTypes.IDENTIFIER)
                if constraint_node.type == TUPLE
                else [constraint_node]
            )
            return ConstrainedTypeParameters(
                name=name,
                constraints=map_t(expression_from_node, constraints),
            )
        case TypeParameterChildrenTypes.SPLAT_TYPE:
            # TODO: match on prefix after merging this with _parse_type_parameters
            prefix = node.children[0]
            return GenericTypeParameter(
                name=expression_from_node(node.children[1]),
            )
