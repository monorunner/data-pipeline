#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions.
"""


def _check_columns(df_to_check, cols) -> None:
    """Check that a list of required column names is in a data frame

    Args:
        df_to_check: A DataFrame to check columns on.
        cols (Iterable[str]): Required columns.
    Returns:
        None
    Raises:
        ValueError: if required cols are not a subset of column names in
            ``df_to_check``.
    Examples:
        >> df = pd.DataFrame({'col_a': [1,2], 'col_b': [2,4]})
        >> check_columns(df, ['col_c'])
        ValueError: Missing columns: `{col_c}`
    """
    if isinstance(cols, str):
        cols = [cols]

    if not set(cols).issubset(df_to_check.columns):
        missing_cols = set(cols).difference(df_to_check.columns)
        raise ValueError(f"Missing columns: `{missing_cols}`.")

    return None
