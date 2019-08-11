#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for the core code.
"""

import pandas as pd
import pandas.testing as tm
import pytest

from dpipe import Pipeline, Filter, ExprAssign, ResetIndex


def test_pipeline_list():

    df = pd.DataFrame({'a': [1, 2, 3, -1, 0]})

    pipeline = Pipeline([Filter('a', lambda x: x >= 0),
                         ExprAssign('b', 'a * 2'),
                         ResetIndex()])

    df_actual = pipeline.apply(df)
    df_expected = pd.DataFrame({'a': [1, 2, 3, 0],
                                'b': [2, 4, 6, 0]})

    tm.assert_frame_equal(df_actual, df_expected)


def test_pipeline_add():

    df = pd.DataFrame({'a': [1, 2, 3, -1, 0]})

    pipeline = (Filter('a', lambda x: x >= 0) +
                ExprAssign('b', 'a * 2') +
                ResetIndex())

    df_actual = pipeline.apply(df)
    df_expected = pd.DataFrame({'a': [1, 2, 3, 0],
                                'b': [2, 4, 6, 0]})

    tm.assert_frame_equal(df_actual, df_expected)


def test_field_check():

    df = pd.DataFrame({'a': [1, 2, 3, -1, 0]})

    with pytest.raises(ValueError):
        Filter('b', lambda x: x >= 0).apply(df)
