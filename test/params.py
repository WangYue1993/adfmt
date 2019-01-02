#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adfmt.params import (
    NestParam,
    SlightParam,
    ParamsMap,
)


def test_nest_param() -> None:
    p = {}

    n1 = NestParam(params=p)
    assert n1.single == {}

    p.update(a='a')
    n2 = NestParam(params=p)
    assert n2.single == {'a': ''}

    p.update(b=[1, 2, 3])
    n3 = NestParam(params=p)
    assert n3.single == {
        'a': '',
        'b': [],
        'b.0': 0,
    }

    p.update(c=dict(c1='c1'))
    n4 = NestParam(params=p)
    assert n4.single == {
        'a': '',
        'b': [],
        'b.0': 0,
        'c': {},
        'c.c1': '',
    }

    p.update(d=[dict(d1='d1', d2=2), dict(d3='d3', d4=4)])
    n5 = NestParam(params=p)
    assert n5.single == {
        'a': '',
        'b': [],
        'b.0': 0,
        'c': {},
        'c.c1': '',
        'd': [],
        'd.0': {},
        'd.0.d1': '',
        'd.0.d2': 0,
    }

    p.update(e=dict(e1=[dict(e2='e2', e3=3, e4=[[4], [5], [6]], e5=dict(e6='e6'))]))
    n6 = NestParam(params=p)
    assert n6.single == {
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
    }


def test_slight_param() -> None:
    p = {}

    s1 = SlightParam(params=p)
    assert s1.slim == {}

    p.update(a=[1, 2, 3])
    s2 = SlightParam(params=p)
    assert s2.slim == {'a': [1]}

    p.update(b=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    s3 = SlightParam(params=p)
    assert s3.slim == {
        'a': [1],
        'b': [[1]],
    }

    p.update(c=[dict(c1='c1', c2=[1, 2]), dict(c3='c3', c4=[3, 4])])
    s4 = SlightParam(params=p)
    assert s4.slim == {
        'a': [1],
        'b': [[1]],
        'c': [{'c1': 'c1', 'c2': [1]}],
    }

    p.update(d=dict(d1={'d11': 'd11'}, d2=[[dict(d22='d22', d33=[1, 2, 3]), dict(d44='d44', d55=[4, 5, 6])]]))
    s5 = SlightParam(params=p)
    assert s5.slim == {
        'a': [1],
        'b': [[1]],
        'c': [{'c1': 'c1', 'c2': [1]}],
        'd': {
            'd1': {'d11': 'd11'},
            'd2': [[{'d22': 'd22', 'd33': [1]}]],
        },
    }


def test_params_map() -> None:
    p = ParamsMap(test='test')
    assert p.test == 'test'

    p.good = 'good'
    assert p.good == 'good'


if __name__ == '__main__':
    test_nest_param()
    test_slight_param()
    test_params_map()
