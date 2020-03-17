from typing import Any


def bad_parameters(*params: str) -> str:
    """
    Generate an error message if the request provides bad parameters (400)

    Args:
        *parameters: The names of the parameters that are invalid
    """
    return f"Must provide query parameter{'s' if len(params) > 1 else ''} {', '.join(params)}"


def internal_server(action: str, model_name: str) -> str:
    """
    Generate an error message if there is an internal server error (500)

    Args:
        action: What action was being done on the database (e.g "save", "retrieve")
        model_name: The name of the model the action was performed on (e.g "TestCase", "TestPlan")
    """
    return f"There was an internal server error while trying to {action} the {model_name} in the database"


def not_found(model_name: str, identifier: Any) -> str:
    """
    Generate an error message if the object is not found (404)

    Args:
        model_name: The name of the model trying to be found (e.g. "TestCase", "TestPlan")
        identifier: The identifier used to find the object on the database (MUST be convertable to str)
    """
    return f"Could not find a {model_name} by identifying it with {identifier}"


def bad_action(action: str, model_name1: str, model_name2: str) -> str:
    """
    Generates an error message for an action between two items

    Args:
        action: What action was being done (e.g. "add", "remove")
        model_name1 & model_name2: The items the action is being performed on
    
    Example Return:
        There was an error while trying to add TestCase -> TestPlan
    """
    return f"The was an error while trying to {action} {model_name1} -> {model_name2}"


def success(model_name: str, action: str) -> str:
    """
    Generates success message when an action completes successfully

    Args:
        model_name: The name of the model that the action successfully completed on
        action: The action (past tense) that successully happened (e.g. "created", "removed")
    """
    return f"{model_name} successfully {action}"
