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


class NestParam(object):
    """
    Assume params (mapping) is a nest collection, which some child-elements are collections too.
    It's not 'friendly' for apiDoc, a simple mapping (none nest-collection elements) is expected.

    NestParam will convert 'nest' to 'simple'.

    The param name will become a complete-layer-location meanwhile.
    That means expanding a relative-name into a complete-name.

    The value of param will be replaced by an init-typing value of itself.

    eg:
    >>> p = NestParam({'mike': {'name': 'mike', 'score': [{'math': 90, 'eng': 85}]}})
    >>> p.single
    {'mike.name': '', 'mike.score.0.math': 0, 'mike.score.0.eng': 0, 'mike.score.0': {}, 'mike.score': [], 'mike': {}}
    >>>
    """

    def __init__(
            self,
            params: Dict,
    ) -> None:
        self._nest = params
        self._single = {}

    @property
    def single(self) -> Dict:
        self._recur_map(affix='', mapping=self._nest)
        return self._single

    def _recur(
            self,
            name: str,
            value: Any,
    ) -> None:
        if isinstance(value, dict):
            self._recur_map(affix=name, mapping=value)

        if isinstance(value, (tuple, list)):
            self._recur_seq(affix=name, sequence=value)

        self._single[name] = type(value)()

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


class SlightParam(object):
    """
    Sometime, the response-params are complicated.
    Lots of child elements repeated with a same construct or a same typing-value confused the developer to look up.

    So complicated-params should be 'slim', which removing the repeated elements.

    eg:
    >>> p = SlightParam({'books': ['b1', 'b2', 'b3', ...]})
    >>> p.slim
    {'books': ['b1']}
    >>>
    """

    def __init__(
            self,
            params: Dict,
    ) -> None:
        self._params = params

    @property
    def slim(self) -> Dict:
        self._recur_map(
            location_chain=[],
            mapping=self._params
        )
        return self._params

    def _recur(
            self,
            location_chain: List,
            child: Any,
    ) -> None:
        if isinstance(child, dict):
            self._recur_map(
                location_chain=location_chain,
                mapping=child,
            )

        if isinstance(child, (tuple, list)):
            self._recur_seq(
                location_chain=location_chain,
                sequence=child,
            )

    def _recur_map(
            self,
            location_chain: List,
            mapping: Dict,
    ) -> None:
        for k, v in mapping.items():
            c = copy.deepcopy(location_chain)
            c.append(f'"{k}"')
            self._recur(
                location_chain=c,
                child=v,
            )

    def _recur_seq(
            self,
            location_chain: List,
            sequence: Sequence,
    ) -> None:
        if sequence:
            single = sequence[:1]
            c = copy.deepcopy(location_chain)

            self._recur(
                location_chain=c,
                child=single[0],
            )

            self.__replace_to_single(
                location_chain=c,
                single=single,
            )


    def __replace_to_single(
            self,
            location_chain: List,
            single: Sequence,
    ) -> Any:
        p = copy.deepcopy(self._params)

        # generate a get-item expression by location-chain
        get_exp = 'p' + ''.join([f'[{key}]' for key in location_chain])
        # set a new single sequence to collection
        set_exp = f'{get_exp} = {single}'
        print(get_exp, location_chain, set_exp)
        exec(set_exp)

        self._params = p


PARAMS_MAP = {}


def params_map_accessor(key: str) -> str:
    v = PARAMS_MAP.get(key, 'ready to fill in ...')
    return v


def update_params_map(
        **kwargs,
) -> None:
    PARAMS_MAP.update(kwargs)
