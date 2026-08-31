from dataclasses import replace

import tree_sitter as ts

from adaptors.treesitter import (
    span_from_node,
    named_child_of,
    type_of,
    types_of,
    only_child_of,
    exec_if_named_child,
    only_type_of,
    expression_from_node,
)
from core.utils import map_t, flatten

from .core import parse_name
from ..ts_nodes.functions import (
    FunctionNodeType,
    FunctionDefinitionFields,
    FunctionDefinitionNodeTypes,
    TypeParameterChildrenTypes,
    TYPE_PARAMETER_NODE_WRAPPER,
    ConstrainedTypeParameterChildrenIndices,
    SplatTypeParameterChildrenIndices,
    SplatTypeParameterPrefixes,
    PARAMETER_NODE_WRAPPER,
    ParameterChildrenTypes,
    TypedParameterChildrenIndices,
    TypedParameterNameTypes,
    TypedDefaultParameterFields,
    DecoratedDefinitionTypes,
)
from ..model.core import (
    TypeParameters,
    PlainTypeParameter,
    ConstrainedTypeParameter,
    BoundTypeParameter,
    Decorator,
)
from ..model.functions import (
    Function,
    Parameters,
    Parameter,
)
from ..ts_nodes.core import CollectionTypes, NameTypes


def parse_function(node: ts.Node) -> Function:
    match FunctionNodeType(node.type):
        case FunctionNodeType.FUNCTION_DEFINITION:
            name = parse_name(named_child_of(node, FunctionDefinitionFields.NAME))
            type_parameters = exec_if_named_child(
                _parse_type_parameters,
                node,
                FunctionDefinitionFields.TYPE_PARAMETERS,
                TypeParameters,
            )
            parameters = exec_if_named_child(
                _parse_parameters,
                node,
                FunctionDefinitionFields.PARAMETERS,
                Parameters,
            )
            is_async = len(type_of(node, FunctionDefinitionNodeTypes.ASYNC)) > 0
            return_type = exec_if_named_child(
                lambda n: expression_from_node(only_child_of(n)),
                node,
                FunctionDefinitionFields.RETURN_TYPE,
                lambda: None,
            )
            return Function(
                name=name,
                span=span_from_node(node),
                body_span=span_from_node(node),
                is_async=is_async,
                type_parameters=type_parameters,
                parameters=parameters,
                return_annotation=return_type,
            )
        case FunctionNodeType.DECORATED_DEFINITION:
            decorators = map_t(
                lambda node: Decorator(
                    body=expression_from_node(node),
                ),
                type_of(
                    node,
                    DecoratedDefinitionTypes.DECORATOR,
                ),
            )
            function = parse_function(
                only_type_of(
                    node,
                    DecoratedDefinitionTypes.DEFINITION,
                )
            )
            return replace(function, decorators=decorators, span=span_from_node(node))


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
                    PlainTypeParameter(
                        name=parse_name(type_param_node),
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
                name = parse_name(name_node)
                if constraint_node.type == CollectionTypes.TUPLE:
                    constraints = type_of(
                        constraint_node, TypeParameterChildrenTypes.IDENTIFIER
                    )
                    param = ConstrainedTypeParameter(
                        name=name,
                        constraints=map_t(parse_name, constraints),
                    )
                else:
                    param = BoundTypeParameter(
                        name=name,
                        bind=parse_name(constraint_node),
                    )
                regulars.append(param)
            case TypeParameterChildrenTypes.SPLAT_TYPE:
                prefix = type_param_node.children[
                    SplatTypeParameterChildrenIndices.PREFIX
                ]
                name = type_param_node.children[SplatTypeParameterChildrenIndices.NAME]
                type_param_node = PlainTypeParameter(
                    name=parse_name(name),
                )
                match SplatTypeParameterPrefixes(prefix.type):
                    case SplatTypeParameterPrefixes.TUPLE:
                        tuples.append(type_param_node)
                    case SplatTypeParameterPrefixes.SPEC:
                        specs.append(type_param_node)
    return TypeParameters(
        regulars=tuple(regulars),
        tuples=tuple(tuples),
        specs=tuple(specs),
    )


def _parse_parameters(node: ts.Node) -> Parameters:
    regulars = []
    positionals = []
    keywords = []
    var_positional = None
    var_keyword = None

    has_positionals = False
    has_keywords = False

    def _bin_parameter(
        has_positional: bool,
        has_keyword: bool,
        parameter: Parameter,
    ) -> None:
        if has_keyword:
            keywords.append(parameter)
        elif has_positional:
            regulars.append(parameter)
        else:
            positionals.append(parameter)

    index = 0
    for child in node.children:
        match child.type:
            case ParameterChildrenTypes.TYPED_PARAMETER:
                variant_node = child.children[TypedParameterChildrenIndices.VARIANT]
                span = span_from_node(child)
                type_node = child.children[TypedParameterChildrenIndices.TYPE]
                annotation = parse_name(only_child_of(type_node))
                match TypedParameterNameTypes(variant_node.type):
                    case TypedParameterNameTypes.IDENTIFIER:
                        _bin_parameter(
                            has_positionals,
                            has_keywords,
                            Parameter(
                                index=index,
                                name=parse_name(variant_node),
                                span=span,
                                annotation=annotation,
                            ),
                        )
                    case TypedParameterNameTypes.LIST_SPLAT:
                        has_keywords = True
                        name = parse_name(
                            only_type_of(variant_node, NameTypes.IDENTIFIER)
                        )
                        var_positional = Parameter(
                            index=index,
                            name=name,
                            span=span,
                            annotation=annotation,
                        )
                    case TypedParameterNameTypes.DICT_SPLAT:
                        name = parse_name(
                            only_type_of(variant_node, NameTypes.IDENTIFIER)
                        )
                        var_keyword = Parameter(
                            index=index,
                            name=name,
                            span=span,
                            annotation=annotation,
                        )
                index += 1
            case ParameterChildrenTypes.POSITIONAL_SEPARATOR:
                has_positionals = True
            case ParameterChildrenTypes.TYPED_DEFAULT_PARAMETER:
                _bin_parameter(
                    has_positionals,
                    has_keywords,
                    Parameter(
                        index=index,
                        name=parse_name(
                            named_child_of(child, TypedDefaultParameterFields.NAME)
                        ),
                        span=span_from_node(child),
                        annotation=parse_name(
                            only_child_of(
                                named_child_of(child, TypedDefaultParameterFields.TYPE)
                            )
                        ),
                        default_value=expression_from_node(
                            named_child_of(child, TypedDefaultParameterFields.VALUE)
                        ),
                    ),
                )
                index += 1
            case ParameterChildrenTypes.IDENTIFIER:
                _bin_parameter(
                    has_positionals,
                    has_keywords,
                    Parameter(
                        index=index,
                        name=parse_name(child),
                        span=span_from_node(child),
                    ),
                )
                index += 1
            case ParameterChildrenTypes.KEYWORD_SEPARATOR:
                has_keywords = True
            case _:
                pass

    if not has_positionals:
        regulars = positionals
        positionals = []

    return Parameters(
        regulars=tuple(regulars),
        positionals=tuple(positionals),
        keywords=tuple(keywords),
        var_positional=var_positional,
        var_keyword=var_keyword,
    )
