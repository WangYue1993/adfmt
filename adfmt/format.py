#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import functools

from typing import (
    Any,
    List,
    Dict,
    Sequence,
    Callable,
    Optional,
    Iterable,
)

from adfmt.enums import (
    ParamTyping,
    BasePermission,
    ApiDoc,
    RequestMethod,
)

from adfmt.params import (
    NestParam,
    SlightParam,
    params_map_accessor,
)

json_dumps_cn: Callable[[Any], str] = functools.partial(
    json.dumps,
    indent=4,
    ensure_ascii=False,
)


def format_class(
        name: str,
        methods: Sequence[str],
) -> str:
    annotation = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n\n'
    statement = f'class ApiDoc{name}(object):'
    body = '\n\n    @staticmethod\n'.join(set(methods))

    content = annotation + statement + body
    return content


def lines_from_join(rows: Iterable) -> str:
    return '\n'.join(rows)


def lines_with_indent(
        content: str,
        indent: Optional[int] = 4,
) -> str:
    rows = content.split('\n')
    indent_rows = [f'{" " * indent}{r}' for r in rows]
    c = lines_from_join(indent_rows)

    return c


def path_of_separate(
        path: str,
        operator: str = '/',
) -> List[str]:
    return path.strip(operator).split(operator)


def typing_by_check(
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


def format_params(
        params: Dict,
        formatter: ApiDoc,
) -> str:
    parts = []
    for param, value in params.items():
        typing = typing_by_check(value)
        explain = params_map_accessor(param)

        f = formatter.param(typing, param, explain)

        if f not in parts:
            parts.append(f)

    # sort by regex. the key-words is the param's name.
    parts.sort(key=lambda x: re.match(r'^(@.+{[A-Za-z]+})\s([\w.]+)\s(.+)$', x).group(2))
    fmt = lines_from_join(parts)
    return fmt


def format_example(
        obj: Any,
        formatter: ApiDoc,
) -> str:
    if obj:
        s = json_dumps_cn(obj)
        lines = lines_with_indent(s)
        fmt = formatter.example(content=lines)
        return fmt
    else:
        return ''


class Formatter(object):

    def __init__(
            self,
            path: str,
            method: RequestMethod,
            title: str,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = BasePermission.NONE,
            header: Optional[Dict] = None,
            params: Optional[Dict] = None,
            success_json: Optional[Dict] = None,
            success_params: Optional[Dict] = None,
            error_json: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
    ) -> None:
        self._path = path
        self._method = method
        self._title = title
        self._desc = desc
        self._group = group
        self._perm = perm
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
        fmt = lines_with_indent(raw)
        return fmt

    def _func_statement(self) -> str:
        parts = path_of_separate(self._path)
        parts.append(self._method.value)

        name = '_'.join(parts)
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
        rows = lines_from_join(check_parts)
        fmt = lines_with_indent(rows)

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
        fmt = format_params(
            params=p,
            formatter=ApiDoc.HEADER,
        )
        return fmt

    def _fmt_header_eg(self) -> str:
        o = self._header
        fmt = format_example(
            obj=o,
            formatter=ApiDoc.HEADER,
        )
        return fmt

    def _fmt_params(self) -> str:
        p = self._params
        fmt = format_params(
            params=p,
            formatter=ApiDoc.PARAM,
        )
        return fmt

    def _fmt_params_eg(self) -> str:
        o = self._params
        fmt = format_example(
            obj=o,
            formatter=ApiDoc.PARAM,
        )
        return fmt

    def _fmt_success(self) -> str:
        p = self._success_params
        fmt = format_params(
            params=p,
            formatter=ApiDoc.SUCCESS,
        )
        return fmt

    def _fmt_success_eg(self) -> str:
        o = self._success_json
        fmt = format_example(
            obj=o,
            formatter=ApiDoc.SUCCESS,
        )
        return fmt

    def _fmt_error(self) -> str:
        p = self._error_params
        fmt = format_params(
            params=p,
            formatter=ApiDoc.ERROR,
        )
        return fmt

    def _fmt_error_eg(self) -> str:
        o = self._error_json
        fmt = format_example(
            obj=o,
            formatter=ApiDoc.ERROR,
        )
        return fmt
