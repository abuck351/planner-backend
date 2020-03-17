from flask import request
from flask_restful import reqparse
from typing import Dict, Any


def _set_defaults(arg_options: Dict, **default_options: Any) -> None:
    """
    Sets default values for a reqparse argument

    Args:
        arg_options: A dictionary where the key is the argument's name
            and the value is a dictionary with reqparse argument options
        **default_options: Keyword arguments for default options to populate
            arg_options if they are not present

    Example: 
        arg_options = {"required": False}
        _set_default(arg_options, type=int, required=True)
        arg_options == {"type": int, "required": False}
    """
    for option, default_value in default_options.items():
        if option not in arg_options:
            arg_options[option] = default_value


def create_parser(**arguments: Dict[str, Any]) -> reqparse.RequestParser:
    """
    Creates a parser to be used in Resources

    Args:
        **arguments: Keyword arguments where the key is the argument's name and
            the value is a dictionary with reqparse argument options

    Returns:
        A reqparse.RequestParser() using the given arguments

    Example:
        create_parser(name={"required": True}, age={"type": int})
    """
    parser = reqparse.RequestParser()
    for arg_name, arg_options in arguments.items():
        _set_defaults(
            arg_options, type=str, required=False, help=f"'{arg_name}' must be supplied"
        )
        parser.add_argument(arg_name, arg_options)
    return parser


def parse_query_params(**params: Dict) -> Dict[str, Any]:
    """
    Creates a dictionary of request.args by only accepting the param if
    it was specified in **params

    Args:
        **params: 
            - The key is the name of the model field
            - The value is a dictionary where the "name" of the query parameter
                is specified as well as the "type" of the query parameter
    
    Example Call:
        query_params = parse_query_params(
            test_case_id={"name": "case_id", "type": int},
            test_plan_id={"name": "plan_id", "type": int},
        )
    """
    query_params = {}
    for model_field, param_options in params.items():
        param = request.args.get(param_options["name"], None)
        if param:
            query_params[model_field] = param_options["type"](param)
    return query_params
