#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import functools

from typing import (
    Any,
    Dict,
    Sequence,
    Callable,
    Optional,
    Iterable,
)

from .enums import (
    ParamTyping,
    BasePermission,
    Permission,
    ApiDoc,
    RequestMethod,
)

from .params import (
    NestParam,
    SlightParam,
)

__all__ = [
    'format_class',
    'Formatter',
]

_json_dumps_cn: Callable[[Any], str] = functools.partial(
    json.dumps,
    indent=4,
    ensure_ascii=False,
)

_DOC_FMT_PATTERN = re.compile(r'^(@.+{[A-Za-z]+})\s([\w.]+)\s(.+)$')

_URL_PATH_PART = re.compile(r'^[A-Za-z0-9]+$')


def format_class(
        name: str,
        methods: Sequence[str],
) -> str:
    statement = f'class ApiDoc{name}(object):'
    body = '\n\n    @staticmethod\n'.join(set(methods))

    content = statement + body
    return content


def _lines_from_join(rows: Iterable) -> str:
    return '\n'.join(rows)


def _lines_with_indent(
        content: str,
        indent: Optional[int] = 4,
) -> str:
    rows = content.split('\n')
    indent_rows = [f'{" " * indent}{r}' for r in rows]
    c = _lines_from_join(indent_rows)

    return c


def _typing_by_check(
        param: Any,
) -> ParamTyping:
    v = param
    if v is True or v is False:
        t = ParamTyping.BOOL

    elif isinstance(v, (int, float)):
        t = ParamTyping.NUM

    elif isinstance(v, str):
        t = ParamTyping.STR

    elif isinstance(v, (list, tuple, set)):
        t = ParamTyping.LIST

    elif isinstance(v, dict):
        t = ParamTyping.OBJ

    else:
        t = ParamTyping.OBJ

    return t


def _format_params(
        params: Dict,
        formatter: ApiDoc,
        mapping: Dict,
) -> str:
    parts = []
    for param, value in params.items():
        typing = _typing_by_check(value)
        explain = mapping.get(param, 'ready to fill in')

        f = formatter.param(typing, param, explain)

        if f not in parts:
            parts.append(f)

    # sorted by regex, key is the name of param which describes absolute location of param.
    parts.sort(key=lambda x: re.match(_DOC_FMT_PATTERN, x).group(2))
    fmt = _lines_from_join(parts)
    return fmt


def _format_example(
        obj: Any,
        formatter: ApiDoc,
) -> str:
    if obj:
        s = _json_dumps_cn(obj)
        lines = _lines_with_indent(s)
        fmt = formatter.example(content=lines)
        return fmt
    else:
        return ''


class EnumMemberError(Exception):
    pass


class Formatter(object):

    def __init__(
            self,
            path: str,
            method: RequestMethod,
            title: str,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.NONE,
            mapping: Optional[Dict] = None,
            header: Optional[Dict] = None,
            params: Optional[Dict] = None,
            success_json: Optional[Dict] = None,
            success_params: Optional[Dict] = None,
            error_json: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
    ) -> None:
        self._path = path

        if not isinstance(method, RequestMethod):
            raise EnumMemberError(
                f'Parameter `perm` expected an {RequestMethod} member, but other was given.'
            )
        self._method = method

        self._title = title
        self._desc = desc
        self._group = group

        if not isinstance(perm, BasePermission):
            raise EnumMemberError(
                f'Parameter `perm` expected an {BasePermission} member or inherit, but other was given.'
            )
        self._perm = perm

        self._map = mapping or {}
        self._header = header or {}
        self._params = params or {}
        self._error_json = error_json or {}
        self._error_params = error_params or {}

        self._success_json = SlightParam(
            success_json
        ).slim or {}

        self._success_params = NestParam(
            success_params
        ).single or {}

    @property
    def doc(self) -> str:
        raw = self._func_statement() + '\n' + self._annotations()
        fmt = _lines_with_indent(raw)
        return fmt

    def _func_statement(self) -> str:
        parts = self._path.strip('/').split('/')
        normals = list(filter(lambda p: re.match(_URL_PATH_PART, p), parts))
        normals.append(self._method.value)

        name = '_'.join(normals)
        fmt = f'def {name}() -> None:'
        return fmt

    def _annotations(self) -> str:
        parts = [
            self._fmt_quotes(),
            self._fmt_declare(),
            self._fmt_description(),
            self._fmt_group(),
            self._fmt_permission(),
            self._fmt_header(),
            self._fmt_header_eg(),
            self._fmt_params(),
            self._fmt_params_eg(),
            self._fmt_success(),
            self._fmt_success_eg(),
            self._fmt_error(),
            self._fmt_error_eg(),
            self._fmt_quotes(),
        ]

        check_parts = filter(lambda x: x, parts)
        rows = _lines_from_join(check_parts)
        fmt = _lines_with_indent(rows)

        return fmt

    @staticmethod
    def _fmt_quotes() -> str:
        return '"""'

    def _fmt_declare(self) -> str:
        fmt = ApiDoc.DECLARE.statement(
            method=self._method,
            path=self._path,
            title=self._title,
        )
        return fmt

    def _fmt_description(self) -> str:
        fmt = ApiDoc.DESC.explain(content=self._desc)
        return fmt

    def _fmt_group(self) -> str:
        fmt = ApiDoc.GROUP.explain(content=self._group)
        return fmt

    def _fmt_permission(self) -> str:
        fmt = ApiDoc.PERM.instruction(
            permit=self._perm,
        )
        return fmt

    def _fmt_header(self) -> str:
        p = self._header
        fmt = _format_params(
            params=p,
            formatter=ApiDoc.HEADER,
            mapping=self._map,
        )
        return fmt

    def _fmt_header_eg(self) -> str:
        o = self._header
        fmt = _format_example(
            obj=o,
            formatter=ApiDoc.HEADER,
        )
        return fmt

    def _fmt_params(self) -> str:
        p = self._params
        fmt = _format_params(
            params=p,
            formatter=ApiDoc.PARAM,
            mapping=self._map,
        )
        return fmt

    def _fmt_params_eg(self) -> str:
        o = self._params
        fmt = _format_example(
            obj=o,
            formatter=ApiDoc.PARAM,
        )
        return fmt

    def _fmt_success(self) -> str:
        p = self._success_params
        fmt = _format_params(
            params=p,
            formatter=ApiDoc.SUCCESS,
            mapping=self._map,
        )
        return fmt

    def _fmt_success_eg(self) -> str:
        o = self._success_json
        fmt = _format_example(
            obj=o,
            formatter=ApiDoc.SUCCESS,
        )
        return fmt

    def _fmt_error(self) -> str:
        p = self._error_params
        fmt = _format_params(
            params=p,
            formatter=ApiDoc.ERROR,
            mapping=self._map,
        )
        return fmt

    def _fmt_error_eg(self) -> str:
        o = self._error_json
        fmt = _format_example(
            obj=o,
            formatter=ApiDoc.ERROR,
        )
        return fmt
