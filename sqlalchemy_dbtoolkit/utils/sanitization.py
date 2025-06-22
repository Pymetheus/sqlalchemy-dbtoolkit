import pandas as pd


def sanitize_nan_to_none(value):
    """
    Converts NaN-like values to None for safe SQL insertion.

    Args:
        value (any): The value to sanitize. Can be of any type, including float, string, or None.

    Returns:
        any: None if the value represents missing data (e.g., np.nan, pd.NA, or the string "NaN");
             otherwise, returns the original value.
    """

    if pd.isna(value):
        return None
    elif isinstance(value, str) and value.strip().lower() == "nan":
        return None
    else:
        return value
