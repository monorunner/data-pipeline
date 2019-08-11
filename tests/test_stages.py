#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for different stages.
"""

import pandas as pd
import pandas.testing as tm
import pytest

from dpipe import TransformCol, ExprAssign, Filter, ResetIndex, \
    DropCols, RenameCols, ReorderCols, QuickEval, __LogShape, __Log


@pytest.fixture
def df():
    df = pd.DataFrame({'a': [1, 2, 3, 5, -1], 'b': list('aabcc')})
    return df


def test_transform_col(df):

    df_in = df.copy()
    df_actual = TransformCol('a', lambda x: 0 if x > 3 else 1).apply(df)
    df_expected = pd.DataFrame({'a': [1, 1, 1, 0, 1], 'b': list('aabcc')})

    tm.assert_frame_equal(df_actual, df_expected)
    tm.assert_frame_equal(df, df_in)


def test_expr_assign(df):

    df_in = df.copy()

    # overwrite existing column
    df_actual = ExprAssign('b', 'a + 1').apply(df)
    df_expected = pd.DataFrame({'a': [1, 2, 3, 5, -1], 'b': [2, 3, 4, 6, 0]})

    tm.assert_frame_equal(df_actual, df_expected)
    tm.assert_frame_equal(df, df_in)

    # assign a new column
    df_actual = ExprAssign('c', 'a').apply(df)
    df_expected = pd.DataFrame({'a': [1, 2, 3, 5, -1], 'b': list('aabcc'),
                                'c': [1, 2, 3, 5, -1]})

    tm.assert_frame_equal(df_actual, df_expected)


def test_filter(df):

    df_actual = Filter('b', lambda x: x != 'a').apply(df)
    df_expected = pd.DataFrame({'a': [3, 5, -1], 'b': list('bcc')},
                               index=[2, 3, 4])

    tm.assert_frame_equal(df_actual, df_expected)


def test_reset_index(df):

    tm.assert_frame_equal(ResetIndex().apply(df), df.reset_index(drop=True))


def test_drop_cols(df):

    tm.assert_frame_equal(DropCols(['b']).apply(df), df[['a']])


def test_rename_cols(df):

    df_in = df.copy()

    tm.assert_frame_equal(RenameCols({'a': 'c'}).apply(df),
                          df.rename(columns={'a': 'c'}))

    tm.assert_frame_equal(RenameCols(['x', 'y']).apply(df),
                          df.rename(columns={'a': 'x', 'b': 'y'}))

    tm.assert_frame_equal(df_in, df)


def test_reorder_cols(df):

    tm.assert_frame_equal(ReorderCols(['b', 'a']).apply(df), df[['b', 'a']])


def test_quick_eval(df):

    tm.assert_frame_equal(QuickEval('a', '>1').apply(df), df[df['a'] > 1])

    df2 = pd.DataFrame({'a': [1, 2, 3, 5, -1], 'b': [2, 3, 4, 1, 1]})
    df_actual = QuickEval('a', '>b').apply(df2)
    df_expected = pd.DataFrame({'a': [5], 'b': [1]}, index=[3])
    tm.assert_frame_equal(df_actual, df_expected)


def test_logs(df):

    tm.assert_frame_equal(df, (__LogShape() + __Log('')).apply(df))
