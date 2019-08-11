#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Minimum viable DataFrame pipeline.
"""

from abc import ABC, abstractmethod

from dpipe.utils import _check_columns


class Stage(ABC):
    """A data transformation pipeline stage."""

    def __add__(self, other):
        """Enable the ``+`` operator for pipeline."""
        if isinstance(other, Pipeline):
            return Pipeline([self, *other.stages])
        elif isinstance(other, Stage):
            return Pipeline([self, other])
        else:
            return NotImplemented

    @abstractmethod
    def _op(self, df):
        """Operations applied to a DataFrame."""
        pass

    def _check(self, df):
        """Checks to run before applying the transformation."""
        cols_to_check = []
        if hasattr(self, 'field'):
            cols_to_check.append(getattr(self, 'field'))
        if hasattr(self, 'fields'):
            cols_to_check += getattr(self, 'fields')
        _check_columns(df, cols_to_check)

    def apply(self, df):
        """Apply the DataFrame transformation."""
        self._check(df)
        return self._op(df)

    __call__ = apply


class Pipeline(Stage):
    """A data transformation pipeline.

    Examples:
        >>> df = pd.DataFrame({'a': [1, 2, 3, 4, -1]})
        >>> Pipeline([__LogShape('Initial shape:'),
        ...           TransformCol('a', lambda x: x * 2),
        ...           ExprAssign('b', 'a+1'),
        ...           ExprAssign('a', 'a-1'),
        ...           Filter('b', lambda x: x > 5),
        ...           __LogShape('After filtering for b:'),
        ...           ResetIndex(),
        ...           __Log('Done.')
        ...           ]).apply(df)
        Initial shape: (5, 1)
        After filtering for b: (2, 2)
        Done.
           a  b
        0  5  7
        1  7  9

    >>> pipeline = QuickEval('a', '>2') + ResetIndex(drop=False)
    >>> pipeline.apply(df)
       index  a
    0      2  3
    1      3  4

    """

    def __init__(self, stages, **kwargs):
        super().__init__(**kwargs)
        self.stages = stages

    def _op(self, df):
        raise NotImplementedError()

    def _check(self, df):
        raise NotImplementedError()

    def apply(self, df):
        prev_df = df
        for stage in self.stages:
            prev_df = stage.apply(prev_df)
        return prev_df
