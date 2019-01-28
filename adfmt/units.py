#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Optional,
    Dict,
    Callable,
    Any,
    Sequence,
)

import os

import urllib.parse
import requests

from .formats import (
    Formatter,
    MulParamsFormatter,
)

from .enums import (
    RequestMethod,
    BasePermission,
    Permission,
)

__all__ = [
    'DocUnit',
]


class InvalidValueError(Exception):
    pass


class DocUnit(object):

    def __init__(
            self,
            name: str,
            domain: str,
            group: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.Nothing,
            mapping: Optional[Dict] = None,
            header_group: Optional[str] = '',
            params_group: Optional[str] = '',
            success_group: Optional[str] = '',
            error_group: Optional[str] = '',
            success_lazy: Optional[Callable] = lambda x: x,
            error_example: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
    ) -> None:
        if not isinstance(name, str) or name == '':
            raise InvalidValueError(
                'Parameter `name` should be a string except "".'
            )
        self._name = name

        if not isinstance(domain, str) or domain == '':
            raise InvalidValueError(
                'Parameter `domain` should be a string except "".'
            )
        self._domain = domain
        # preset default attributes for request-methods: get and post
        self._group = group
        self._perm = perm
        self._mapping = mapping
        self._success_lazy = success_lazy
        self._error_example = error_example or {}
        self._error_params = error_params or {}
        # group name
        self._header_group = header_group
        self._params_group = params_group
        self._success_group = success_group
        self._error_group = error_group
        # repeated doc methods are useless, so use the set container.
        self._doc_methods = set()

    def get(
            self,
            path: str,
            title: str,
            # optional
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.Nothing,
            mapping: Optional[Dict] = None,
            # group name
            header_group: Optional[str] = '',
            params_group: Optional[str] = '',
            success_group: Optional[str] = '',
            error_group: Optional[str] = '',
            # params and examples
            success_lazy: Optional[Callable] = lambda x: x,
            error_example: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
            **kwargs
    ) -> Any:
        # using requests-post
        url = urllib.parse.urljoin(self._domain, path)
        r = requests.get(
            url=url,
            **kwargs,
        )
        # ready for Formatter
        _path = path
        _title = title
        _method = RequestMethod.Get

        _desc = desc
        _group = group or self._group
        _perm = perm or self._perm

        _mapping = mapping or self._mapping

        _header = kwargs.get('headers', {})
        _header_group = header_group or self._header_group

        _params = {}
        _params.update(kwargs.get('params', {}))
        _params_group = params_group or self._params_group

        _success_lazy = success_lazy or self._success_lazy
        _success_params = _success_lazy(r.json())
        _success_example = r.json()
        _success_group = success_group or self._success_group

        _error_params = error_params or self._error_params
        _error_example = error_example or self._error_example
        _error_group = error_group or self._error_group

        doc = Formatter(
            path=_path,
            method=_method,
            title=_title,
            group=_group,
            desc=_desc,
            perm=_perm,
            mapping=_mapping,
            header=_header,
            header_group=_header_group,
            params=_params,
            params_group=_params_group,
            success_example=_success_example,
            success_params=_success_params,
            success_group=_success_group,
            error_example=_error_example,
            error_params=_error_params,
            error_group=_error_group,
        ).doc

        self._doc_methods.add(doc)

        return r, doc

    def post(
            self,
            path: str,
            title: str,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.Nothing,
            mapping: Optional[Dict] = None,
            header_group: Optional[str] = '',
            params_group: Optional[str] = '',
            success_group: Optional[str] = '',
            error_group: Optional[str] = '',
            success_lazy: Optional[Callable] = lambda x: x,
            error_example: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
            **kwargs
    ) -> Any:
        # using requests-post
        url = urllib.parse.urljoin(self._domain, path)
        r = requests.post(
            url=url,
            **kwargs,
        )
        # ready for Formatter
        _path = path
        _title = title
        _method = RequestMethod.Post

        _desc = desc
        _group = group or self._group
        _perm = perm or self._perm

        _mapping = mapping or self._mapping

        _header = kwargs.get('headers', {})
        _header_group = header_group or self._header_group

        _params = {}
        _params.update(kwargs.get('data', {}))
        _params.update(kwargs.get('json', {}))
        _params_group = params_group or self._params_group

        _success_lazy = success_lazy or self._success_lazy
        _success_params = _success_lazy(r.json())
        _success_example = r.json()
        _success_group = success_group or self._success_group

        _error_params = error_params or self._error_params
        _error_example = error_example or self._error_example
        _error_group = error_group or self._error_group

        doc = Formatter(
            path=_path,
            method=_method,
            title=_title,
            group=_group,
            desc=_desc,
            perm=_perm,
            mapping=_mapping,
            header=_header,
            header_group=_header_group,
            params=_params,
            params_group=_params_group,
            success_example=_success_example,
            success_params=_success_params,
            success_group=_success_group,
            error_example=_error_example,
            error_params=_error_params,
            error_group=_error_group,
        ).doc

        self._doc_methods.add(doc)

        return r, doc

    def get_many(
            self,
            path: str,
            title: str,
            mul_kw: Optional[Sequence[Dict]] = None,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.Nothing,
            mapping: Optional[Dict] = None,
            mul_groups: Optional[Sequence[str]] = None,
            mul_header_groups: Optional[Sequence[str]] = None,
            mul_params_groups: Optional[Sequence[str]] = None,
            mul_success_groups: Optional[Sequence[str]] = None,
            mul_error_groups: Optional[Sequence[str]] = None,
            success_lazy: Optional[Callable] = lambda x: x,
            error_example: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
    ) -> Any:
        """"""
        many_response = []
        for m in mul_kw:
            # using requests-post
            url = urllib.parse.urljoin(self._domain, path)
            r = requests.get(
                url=url,
                **m,
            )

            many_response.append(r)




        # ready for Formatter
        _path = path
        _title = title
        _method = RequestMethod.Get

        _desc = desc
        _group = group or self._group
        _perm = perm or self._perm

        _mapping = mapping or self._mapping

        _header = kwargs.get('headers', {})
        _header_group = header_group or self._header_group

        _params = {}
        _params.update(kwargs.get('params', {}))
        _params_group = params_group or self._params_group

        _success_lazy = success_lazy or self._success_lazy
        _success_params = _success_lazy(r.json())
        _success_example = r.json()
        _success_group = success_group or self._success_group

        _error_params = error_params or self._error_params
        _error_example = error_example or self._error_example
        _error_group = error_group or self._error_group


    @property
    def output(self) -> str:
        case_name = _camel_cased_word(self._name)
        statement = f'class ApiDoc{case_name}(object):'

        methods = list(self._doc_methods)
        methods.sort(key=lambda x: x)
        body = '\n\n    @staticmethod\n'.join(methods)

        code = statement + body
        return code

    def write_on(
            self,
            directory: str,
    ) -> None:
        """
        It's hard to keep a balance between design of original intention and developer custom,
        so the simplest way is 'do nothing'.

        That means design an original and simple way which with none of predicting to what and how user using.

        :param directory: instead of taking a relative path or name, an absolute folder path is required.
        :return: None
        """
        annotation = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n\n'
        code = self.output
        content = annotation + code

        path = os.path.join(directory, f'{self._name}.py')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


def _camel_cased_word(word: str) -> str:
    return word[0].upper() + word[1:]
