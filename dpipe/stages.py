#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic pipeline stages.

Index:
    TransformCol
    ExprAssign
    Filter
    ResetIndex
    DropCols
    RenameCols
    ReorderCols
    QuickEval
    __LogShape
    __Log

"""

from dpipe.core import Stage


# <transformation> ------------------------------------------------------------
class TransformCol(Stage):
    """Transform an existing column with a function."""
    def __init__(self, field: str, fn: callable):
        self.field = field
        self.fn = fn

    def _op(self, df):
        df = df.copy()
        df[self.field] = df[self.field].map(self.fn)
        return df


class ExprAssign(Stage):
    """Assign or change a column with a string expression."""
    def __init__(self, field: str, expr: str):
        self.field = field
        self.expr = expr

    def _op(self, df):
        df = df.copy()
        df[self.field] = df.eval(self.expr)
        return df

    def _check(self, df):
        # overwrite because the `field` can be a new field
        pass


class Filter(Stage):
    """Filter an existing column with a function."""
    def __init__(self, field: str, fn: callable):
        self.field = field
        self.fn = fn

    def _op(self, df):
        return df[self.fn(df[self.field])]

# </transformation> -----------------------------------------------------------


# <pd-methods> ----------------------------------------------------------------
class ResetIndex(Stage):
    """Calls pandas ``reset_index()``."""
    def __init__(self, drop=True, **kwargs):
        self.drop = drop
        self.kwargs = kwargs

    def _op(self, df):
        return df.reset_index(drop=self.drop, **self.kwargs)

# </pd-methods> ---------------------------------------------------------------


# <col-change> ----------------------------------------------------------------
class DropCols(Stage):
    """Drop existing columns."""
    def __init__(self, fields: list):
        self.fields = fields

    def _op(self, df):
        return df.drop(columns=self.fields)


class RenameCols(Stage):
    """Rename existing columns with a dictionary of a list of names."""
    def __init__(self, col_names: (dict, list)):
        self.col_names = col_names

    def _op(self, df):
        if isinstance(self.col_names, dict):
            return df.rename(columns=self.col_names)
        else:
            if len(df.columns) != len(self.col_names):
                raise ValueError(f'{len(df.columns)} columns but '
                                 f'{len(self.col_names)} names provided.')
            df = df.copy()
            df.columns = self.col_names
            return df


class ReorderCols(Stage):
    """Reorder existing columns."""
    def __init__(self, col_order: list):
        self.col_order = col_order

    def _op(self, df):
        if len(df.columns) != len(self.col_order):
            raise ValueError(f'{len(df.columns)} columns in data but '
                             f'{len(self.col_order)} names provided.')
        return df[self.col_order]

# </col-change>----------------------------------------------------------------


# <shortcuts> -----------------------------------------------------------------
class QuickEval(Stage):
    """Shortcut for an ``eval()`` expression.

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'a':  [1, 2, 3, 4, 0]})
        >>> QuickEval('a', '>1').apply(df)
           a
        1  2
        2  3
        3  4

    """
    def __init__(self, field: str, expr: str):
        self.field = field
        self.expr = field + expr

    def _op(self, df):
        return df[df.eval(self.expr)]

# </shortcuts> ----------------------------------------------------------------


# <logs> ----------------------------------------------------------------------
class __LogShape(Stage):
    """Log the shape of the DataFrame."""
    def __init__(self, msg=''):
        self.msg = msg

    def _op(self, df):
        print(self.msg, df.shape)
        return df


class __Log(Stage):
    """Log with custom messages."""
    def __init__(self, msg: str = ''):
        self.msg = msg

    def _op(self, df):
        print(self.msg)
        return df

# </logs> ---------------------------------------------------------------------
