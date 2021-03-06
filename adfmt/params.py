#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    Sequence,
    List,
    Union,
)

import copy

__all__ = [
    'FlatMap',
    'SingleMap',
    'ParamsMap',
]


class ParamsTypeError(Exception):
    pass


class FlatMap(object):
    """
    params (map) api returned is a nest collection usually,
    which some child elements may be collections too.

    It's not 'friendly' for writing apiDoc,
    the complicated locations information of all params need to be writing manually.

    The `FlatMap` will convert 'nest' to 'flat'.

    During converting:
        > The param name (key) will be expanding into a complete layer location.

        > Value of param will be replaced by a default value of type for itself.

    eg:
    >>> p = FlatMap({'mike': {'name': 'mike', 'score': [{'math': 90, 'eng': 85}]}})
    >>> p.flat
    {'mike.name': '', 'mike.score.0.math': 0, 'mike.score.0.eng': 0, 'mike.score.0': {}, 'mike.score': [], 'mike': {}}
    >>>
    """

    def __init__(
            self,
            params: Dict,
    ) -> None:
        if not isinstance(params, dict):
            raise ParamsTypeError(
                'Parameter `params` expected a "dict", but other was given.'
            )
        self._nest = params

        self._flat = {}

    @property
    def flat(self) -> Dict:
        self._recur_map(affix='', mapping=self._nest)
        return self._flat

    def _recur(
            self,
            name: str,
            value: Any,
    ) -> None:
        if isinstance(value, dict):
            self._recur_map(affix=name, mapping=value)

        if isinstance(value, (tuple, list)):
            self._recur_seq(affix=name, sequence=value)

        self._flat[name] = type(value)()

    def _recur_map(
            self,
            affix: str,
            mapping: Dict,
    ) -> None:
        for k, v in mapping.items():
            if affix:
                name = f'{affix}.{k}'
            else:
                name = k
            self._recur(name=name, value=v)

    def _recur_seq(
            self,
            affix: str,
            sequence: Sequence,
    ) -> None:
        if sequence:
            name = f'{affix}.0'
            self._recur(name=name, value=sequence[0])


class SingleMap(object):
    """
    Sometime, the response params (map) are complicated.
    Lots of child elements repeated with a same construct or a same type value disturb the developer to look up.

    So complicated params should be 'slim', which means removing the repeated elements.

    eg:
    >>> p = SingleMap({'books': ['b1', 'b2', 'b3', ...]})
    >>> p.single
    {'books': ['b1']}
    >>>
    """

    def __init__(
            self,
            params: Dict,
    ) -> None:
        if not isinstance(params, dict):
            raise ParamsTypeError(
                'Parameter `params` expected a "dict", but other was given.'
            )
        self._params = params

    @property
    def single(self) -> Dict:
        self._recur_map(
            location_chain=[],
            mapping=self._params
        )
        return self._params

    def _recur(
            self,
            location_chain: List,
            child: Any,
            key: Union[str, int],
    ) -> None:
        """
        `location_chain` save 'key' and 'order of get item' for collection.

        In python, both collections <Dict> and <List> have the special methods `__getitem__` and `__setitem__`.

        It makes the collection easy to get item and set item,
        through square brackets of symbol `[key]` enclosing a key (index).
        eg:
        >>> a = {'a': 'a'}
        >>> a['a']
        'a'
        >>> a['b'] = 'b'
        >>> a
        {'a': 'a', 'b': 'b'}
        >>> b = [1, 2, 3]
        >>> b[0]
        1
        >>> b[0] = 2
        >>> b
        [2, 2, 3]
        >>>

        Thus, `location_chain` can be used to make up the expression of setting item or getting item.

        Additionally, a deepcopy (clone a same object) of `location_chain` is required for every child element.
        It can guarantee every child element own the `location_chain` itself, and escape interference from each other.

        Without doing that, the shared `location_chain` which every element can change will be mess,
        and it may bring an unexpected result or an error.
        """
        if isinstance(child, dict):
            c = copy.deepcopy(location_chain)
            c.append(key)
            self._recur_map(
                location_chain=c,
                mapping=child,
            )

        if isinstance(child, (tuple, list)):
            c = copy.deepcopy(location_chain)
            c.append(key)
            self._recur_seq(
                location_chain=c,
                sequence=child,
            )

    def _recur_map(
            self,
            location_chain: List,
            mapping: Dict,
    ) -> None:
        for k, v in mapping.items():
            key = f'"{k}"'
            self._recur(
                location_chain=location_chain,
                child=v,
                key=key,
            )

    def _recur_seq(
            self,
            location_chain: List,
            sequence: Sequence,
    ) -> None:
        if sequence:
            flat = sequence[:1]

            self.__replace_to_flat(
                location_chain=location_chain,
                flat=flat,
            )

            self._recur(
                location_chain=location_chain,
                child=flat[0],
                key=0,
            )

    def __replace_to_flat(
            self,
            location_chain: List,
            flat: Sequence,
    ) -> Any:
        p = copy.deepcopy(self._params)

        # generate a get-item expression by location-chain
        get_exp = 'p' + ''.join([f'[{key}]' for key in location_chain])
        # set a new flat sequence to collection
        set_exp = f'{get_exp} = {flat}'
        exec(set_exp)

        self._params = p


class ParamsMap(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value
