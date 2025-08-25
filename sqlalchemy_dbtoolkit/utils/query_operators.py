import operator

COMPARISON_OPERATORS = {
    'eq': operator.eq,   # ==
    'ne': operator.ne,   # !=
    'gt': operator.gt,   # >
    'lt': operator.lt,   # <
    'ge': operator.ge,   # >=
    'le': operator.le,   # <=
    'like': lambda c, v: c.like(v),   # Pattern%
    'ilike': lambda c, v: c.ilike(v),   # Pattern%
    'in': lambda c, v: c.in_(v),   # [value, value]
    'not_in': lambda c, v: ~c.in_(v)   # [value, value]
}


def get_filter_operator(operator_name: str):
    """
    Retrieves and validates a filter operator function.

    Args:
        operator_name (str): The name of the operator (e.g., "eq", "gt", "like").

    Returns:
        callable: A function that applies the operator to a column and value.

    Raises:
        ValueError: If the operator is not supported.
        TypeError: If operator_name is not a string.
    """

    if not isinstance(operator_name, str):
        raise TypeError(f"{operator_name} must be a string")

    op = COMPARISON_OPERATORS.get(operator_name)

    if op is None:
        raise ValueError(f"Unsupported operator: {operator_name}")
    return op
