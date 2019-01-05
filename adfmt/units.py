#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import (
    Optional,
    Dict,
    Callable,
    Any,
)

import os

import urllib.parse
import requests

from .format import Formatter

from .enums import (
    RequestMethod,
    BasePermission,
    Permission,
)


class DocUnit(object):

    def __init__(
            self,
            name: str,
            domain: str,
            group: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.NONE,
            mapping: Optional[Dict] = None,
            success_lazy: Optional[Callable] = lambda x: x,
            error_json: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
    ) -> None:
        self._name = name
        self._domain = domain
        self._group = group
        self._perm = perm
        self._mapping = mapping
        self._success_lazy = success_lazy
        self._error_json = error_json or {}
        self._error_params = error_params or {}

        self._doc_methods = []

    def get(
            self,
            path: str,
            title: str,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.NONE,
            mapping: Optional[Dict] = None,
            success_lazy: Optional[Callable] = lambda x: x,
            error_json: Optional[Dict] = None,
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
        _method = RequestMethod.GET

        _desc = desc
        _group = group or self._group
        _perm = perm or self._perm

        _mapping = mapping or self._mapping

        _header = kwargs.get('headers', {})

        _params = {}
        _params.update(kwargs.get('params', {}))

        _success_lazy = success_lazy or self._success_lazy
        _success_params = _success_lazy(r.json())
        _success_json = r.json()

        _error_params = error_params or self._error_params
        _error_json = error_json or self._error_json

        doc = Formatter(
            path=_path,
            method=_method,
            title=_title,
            group=_group,
            desc=_desc,
            perm=_perm,
            mapping=_mapping,
            header=_header,
            params=_params,
            success_json=_success_json,
            success_params=_success_params,
            error_json=_error_json,
            error_params=_error_params,
        ).doc

        if doc not in self._doc_methods:
            self._doc_methods.append(doc)

        return r

    def post(
            self,
            path: str,
            title: str,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.NONE,
            mapping: Optional[Dict] = None,
            success_lazy: Optional[Callable] = lambda x: x,
            error_json: Optional[Dict] = None,
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
        _method = RequestMethod.POST

        _desc = desc
        _group = group or self._group
        _perm = perm or self._perm

        _mapping = mapping or self._mapping

        _header = kwargs.get('headers', {})

        _params = {}
        _params.update(kwargs.get('data', {}))
        _params.update(kwargs.get('json', {}))

        _success_lazy = success_lazy or self._success_lazy
        _success_params = _success_lazy(r.json())
        _success_json = r.json()

        _error_params = error_params or self._error_params
        _error_json = error_json or self._error_json

        doc = Formatter(
            path=_path,
            method=_method,
            title=_title,
            group=_group,
            desc=_desc,
            perm=_perm,
            mapping=_mapping,
            header=_header,
            params=_params,
            success_json=_success_json,
            success_params=_success_params,
            error_json=_error_json,
            error_params=_error_params,
        ).doc

        if doc not in self._doc_methods:
            self._doc_methods.append(doc)

        return r

    @property
    def output(self) -> str:
        statement = f'class ApiDoc{self._name}(object):'
        body = '\n\n    @staticmethod\n'.join(set(self._doc_methods))
        code = statement + body
        return code

    def write_on(
            self,
            directory: str,
    ) -> None:
        annotation = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n\n'
        code = self.output
        content = annotation + code

        path = os.path.join(directory, f'{self._name}.py')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
