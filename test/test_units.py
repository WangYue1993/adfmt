#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from adfmt.units import (
    DocUnit,
    InvalidValueError,
)


class TestDocUnit(unittest.TestCase):

    def test_get(self) -> None:
        pass

    def test_post(self) -> None:
        pass

    def test_output(self) -> None:
        pass

    def test_write(self) -> None:
        pass

    def test_exception_name_error(self) -> None:
        self.assertRaises(
            InvalidValueError,
            DocUnit,
            domain='http://test.com/',
            name='',
        )

    def test_exception_domain_error(self) -> None:
        self.assertRaises(
            InvalidValueError,
            DocUnit,
            name='test',
            domain='',
        )
