import uuid


def is_valid_uuid(val):
    """Проверяет на валидность UUID."""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def get_or_create(session, model, **kwargs):
    """Возвращает объект модели если он существует или создаёт новый."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
