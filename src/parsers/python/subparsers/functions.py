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
    TYPE_PARAMETER_NODE_WRAPPER,
    ConstrainedTypeParameterChildrenIndices,
    SplatTypeParameterChildrenIndices,
    SplatTypeParameterPrefixes,
)
from ..model.functions import (
    Function,
    TypeParameter,
    TypeParameters,
    GenericTypeParameter,
    ConstrainedTypeParameter,
    BoundTypeParameter,
)
from ..ts_nodes.core import CollectionTypes


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
    regulars = []
    tuples = []
    specs = []
    for child in type_of(node, TYPE_PARAMETER_NODE_WRAPPER):
        type_param_node = only_child_of(child)
        # NOTE: current python treesitter grammar is 3.12 so defaults can't be parsed yet
        match TypeParameterChildrenTypes(type_param_node.type):
            case TypeParameterChildrenTypes.IDENTIFIER:
                regulars.append(
                    GenericTypeParameter(
                        name=expression_from_node(type_param_node),
                    )
                )
            case TypeParameterChildrenTypes.CONSTRAINED_TYPE:
                name_node = only_child_of(
                    type_param_node.children[
                        ConstrainedTypeParameterChildrenIndices.NAME
                    ]
                )
                constraint_node = only_child_of(
                    type_param_node.children[
                        ConstrainedTypeParameterChildrenIndices.CONSTRAINTS
                    ]
                )
                name = expression_from_node(name_node)
                if constraint_node.type == CollectionTypes.TUPLE:
                    constraints = type_of(
                        constraint_node, TypeParameterChildrenTypes.IDENTIFIER
                    )
                    param = ConstrainedTypeParameter(
                        name=name,
                        constraints=map_t(expression_from_node, constraints),
                    )
                else:
                    param = BoundTypeParameter(
                        name=name,
                        bind=expression_from_node(constraint_node),
                    )
                regulars.append(param)
            case TypeParameterChildrenTypes.SPLAT_TYPE:
                prefix = type_param_node.children[
                    SplatTypeParameterChildrenIndices.PREFIX
                ]
                name = type_param_node.children[SplatTypeParameterChildrenIndices.NAME]
                type_param_node = GenericTypeParameter(
                    name=expression_from_node(name),
                )
                match SplatTypeParameterPrefixes(prefix.type):
                    case SplatTypeParameterPrefixes.TUPLE:
                        tuples.append(type_param_node)
                    case SplatTypeParameterPrefixes.SPEC:
                        specs.append(type_param_node)
    return TypeParameters(
        regular=tuple(regulars),
        tuple=tuple(tuples),
        spec=tuple(specs),
    )
