from datetime import datetime



def datetime_to_string(dt: datetime, format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Convert a datetime object to a string.

    Parameters:
    dt (datetime): The datetime object to convert.
    format (str): The format string to use for conversion. Default is '%Y-%m-%d %H:%M:%S'.

    Returns:
    str: The formatted datetime string.
    """
    return dt.strftime(format)