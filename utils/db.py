from flask_sqlalchemy import SQLAlchemy
from typing import ClassVar, Dict, Any

db = SQLAlchemy()


def find_by(model_cls: ClassVar[db.Model], **filter_properties) -> [db.Model]:
    """
    Finds all instances from the database given filter_properties

    Args:
        model_cls: The model class to be searched from
        **filter_properties: The properties of model_cls, specified as keyword
            arguements, to use to filter_by (returns all if no filter_properties
            are provided)

    Returns:
        A list of instances of the model class if found, else None
    """
    if filter_properties:
        return model_cls.query.filter_by(**filter_properties)
    return model_cls.query.all()


def save(model: db.Model) -> None:
    """
    Saves a model to the database

    Args:
        model: The model instance to be saved
    """
    db.session.add(model)
    db.session.commit()


def delete(model: db.Model) -> None:
    """
    Deletes a model from the database

    Args:
        model: The model instance to be deleted
    """
    db.session.delete(model)
    db.session.commit()


def update(model: db.Model, **fields: Dict[str, Any]) -> None:
    """
    Updates a model instance given the fields and values as keyword arguments

    Args:
        model: The model instance to be updated
        **fields: The fields to update the object with (e.g. name="Aaron")
    """
    for field, value in fields.items():
        if hasattr(model, field):
            setattr(model, field, value)
    db.session.commit()
