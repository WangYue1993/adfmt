#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from adfmt.params import (
    FlatMap,
    SingleMap,
    ParamsMap,
    ParamsTypeError,
)


class TestNestToSingle(unittest.TestCase):
    p = {}

    def test_nest_param_1(self) -> None:
        p = self.p

        n1 = FlatMap(params=p)
        self.assertEqual(n1.flat, {})

    def test_nest_param_2(self) -> None:
        p = self.p
        p.update(a='a')

        n2 = FlatMap(params=p)
        self.assertEqual(n2.flat, {'a': ''})

    def test_nest_param_3(self) -> None:
        p = self.p
        p.update(b=[1, 2, 3])

        n3 = FlatMap(params=p)
        self.assertEqual(
            n3.flat,
            {
                'a': '',
                'b': [],
                'b.0': 0,
            },
        )

    def test_nest_param_4(self) -> None:
        p = self.p
        p.update(c=dict(c1='c1'))

        n4 = FlatMap(params=p)
        self.assertEqual(
            n4.flat,
            {
                'a': '',
                'b': [],
                'b.0': 0,
                'c': {},
                'c.c1': '',
            },
        )

    def test_nest_param_5(self) -> None:
        p = self.p
        p.update(
            d=[
                dict(d1='d1', d2=2),
                dict(d3='d3', d4=4),
            ]
        )

        n5 = FlatMap(params=p)
        self.assertEqual(
            n5.flat,
            {
                'a': '',
                'b': [],
                'b.0': 0,
                'c': {},
                'c.c1': '',
                'd': [],
                'd.0': {},
                'd.0.d1': '',
                'd.0.d2': 0,
            },
        )

    def test_nest_param_6(self) -> None:
        p = self.p
        p.update(e=dict(e1=[
            dict(e2='e2',
                 e3=3,
                 e4=[[4], [5], [6]],
                 e5=dict(e6='e6')
                 )
        ]))

        n6 = FlatMap(params=p)
        self.assertEqual(n6.flat, {
            'a': '',
            'b.0': 0,
            'b': [],
            'c.c1': '',
            'c': {},
            'd.0.d1': '',
            'd.0.d2': 0,
            'd.0': {},
            'd': [],
            'e.e1.0.e2': '',
            'e.e1.0.e3': 0,
            'e.e1.0.e4.0.0': 0,
            'e.e1.0.e4.0': [],
            'e.e1.0.e4': [],
            'e.e1.0.e5.e6': '',
            'e.e1.0.e5': {},
            'e.e1.0': {},
            'e.e1': [],
            'e': {},
        })

    def test_exception_value_error(self) -> None:
        self.assertRaises(
            ParamsTypeError,
            FlatMap,
            params='',
        )


class TestComplicatedToSlight(unittest.TestCase):
    p = {}

    def test_slight_param_1(self) -> None:
        p = self.p

        s1 = SingleMap(params=p)
        self.assertEqual(s1.single, {})

    def test_slight_param_2(self) -> None:
        p = self.p
        p.update(a=[1, 2, 3])

        s2 = SingleMap(params=p)
        self.assertEqual(s2.single, {'a': [1]})

    def test_slight_param_3(self) -> None:
        p = self.p
        p.update(b=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])

        s3 = SingleMap(params=p)
        self.assertEqual(
            s3.single,
            {
                'a': [1],
                'b': [[1]],
            },
        )

    def test_slight_param_4(self) -> None:
        p = self.p
        p.update(c=[
            dict(c1='c1', c2=[1, 2]),
            dict(c3='c3', c4=[3, 4]),
        ])

        s4 = SingleMap(params=p)
        self.assertEqual(
            s4.single,
            {
                'a': [1],
                'b': [[1]],
                'c': [{'c1': 'c1', 'c2': [1]}],
            },
        )

    def test_slight_param_5(self) -> None:
        p = self.p
        p.update(
            d=dict(
                d1={'d11': 'd11'},
                d2=[[
                    dict(
                        d22='d22',
                        d33=[1, 2, 3],
                    ),
                    dict(
                        d44='d44',
                        d55=[4, 5, 6],
                    ),
                ]],
            ),
        )

        s5 = SingleMap(params=p)
        self.assertEqual(
            s5.single,
            {
                'a': [1],
                'b': [[1]],
                'c': [{'c1': 'c1', 'c2': [1]}],
                'd': {
                    'd1': {'d11': 'd11'},
                    'd2': [[{'d22': 'd22', 'd33': [1]}]],
                },
            },
        )

    def test_exception_value_error(self) -> None:
        self.assertRaises(
            ParamsTypeError,
            SingleMap,
            params='',
        )


class TestParamMap(unittest.TestCase):
    p = ParamsMap(test='test')

    def test_accessor(self) -> None:
        p = self.p

        self.assertEqual(p.test, 'test')

    def test_mutator(self) -> None:
        p = self.p

        p.good = 'good'
        self.assertEqual(p.good, 'good')


if __name__ == '__main__':
    unittest.main()
