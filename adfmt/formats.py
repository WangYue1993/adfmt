#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import functools

from typing import (
    Any,
    Dict,
    List,
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
    'formatted_class',
    'Formatter',
]

_json_dumps_cn: Callable[[Any], str] = functools.partial(
    json.dumps,
    indent=4,
    ensure_ascii=False,
)

# used for match api-doc `@apiParam {type} [(group)] [param] [explain]` (and header, success, error)
_DOC_FMT_PATTERN = re.compile(r'^(@api[A-Za-z]+)\s(\(.+\))?\s?({[A-Za-z]+})\s([\w]+)\s')

# query params of path should be ignored.
_URL_PATH_PATTERN = re.compile(r'^(/[^?]+)\??')

# func name
_FUNC_NAME_PATTERN = re.compile(r'^[_A-Za-z][A-Za-z0-9_]*')


def formatted_class(
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
        t = ParamTyping.Bool

    elif isinstance(v, (int, float)):
        t = ParamTyping.Num

    elif isinstance(v, str):
        t = ParamTyping.Str

    elif isinstance(v, (list, tuple, set)):
        t = ParamTyping.List

    elif isinstance(v, dict):
        t = ParamTyping.Obj

    else:
        t = ParamTyping.Obj

    return t


def _formatted_params(
        params: Dict,
        formatter: ApiDoc,
        mapping: Dict,
        group: str,
) -> str:
    if group:
        fmt_group = f'({group})'
    else:
        fmt_group = group

    parts = set()
    for param, value in params.items():
        typing = _typing_by_check(value)
        explain = mapping.get(param, 'ready to fill in')

        f = formatter.param(
            typing=typing,
            name=param,
            explain=explain,
            group=fmt_group,
        )

        parts.add(f)

    parts = list(parts)
    _sort_with_abc(parts)

    fmt = _lines_from_join(parts)
    return fmt


def _formatted_example(
        obj: Any,
        formatter: ApiDoc,
        group: str,
) -> str:
    if obj:
        s = _json_dumps_cn(obj)
        lines = _lines_with_indent(s)

        names = [
            formatter.name.lower(),
            'example',
        ]
        if group:
            names.append(group)

        fmt = formatter.example(
            content=lines,
            name='-'.join(names),
        )
        return fmt

    else:
        return ''


def _sort_with_abc(seq: List) -> None:
    """
    sorted by regex and alphabet, and key is the name of param which describes absolute location of param.
    :param seq:
    :return: None
    """
    seq.sort(key=lambda x: re.match(_DOC_FMT_PATTERN, x).group(4))


def _fixed_path(
        path: str,
) -> str:
    """
    Url path will be matched by Re-pattern expression to find out the legal path wanted,

    Double slashes '//' (or more) will be replaced by single.
    """
    replaced = re.sub(r'/+', '/', path)

    r = re.match(_URL_PATH_PATTERN, replaced)
    if not r:
        raise NotLegalPathError(
            f'Parameter `path` is illegal, unexpected value `{path}` was given, checkout your path.'
        )

    find = r.group(1)

    return find


def _parts_from_split(
        path: str,
) -> List[str]:
    """
    Split path will be using for making up function name.
    """
    parts = path.strip('/').split('/')

    legals = list(filter(lambda x: re.match(_FUNC_NAME_PATTERN, x), parts))
    return legals


class NotLegalPathError(Exception):
    pass


class EnumMemberError(Exception):
    pass


class Formatter(object):
    def __init__(
            self,
            path: str,
            method: RequestMethod,
            title: str,
            # optional
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.Nothing,
            # params map
            mapping: Optional[Dict] = None,
            # header example and params
            header: Optional[Dict] = None,
            header_group: Optional[str] = '',
            # param example and params
            params: Optional[Dict] = None,
            params_group: Optional[str] = '',
            # success example and params
            success_example: Optional[Dict] = None,
            success_params: Optional[Dict] = None,
            success_group: Optional[str] = '',
            # error example and params
            error_example: Optional[Dict] = None,
            error_params: Optional[Dict] = None,
            error_group: Optional[str] = '',
    ) -> None:
        self._path = _fixed_path(path)

        if not isinstance(method, RequestMethod):
            raise EnumMemberError(
                f'Parameter `perm` expected an {RequestMethod} member, but other was given.'
            )
        self._method = method

        self._title = title
        self._desc = desc
        self._group = group

        self._header_group = header_group
        self._params_group = params_group
        self._success_group = success_group
        self._error_group = error_group

        if not isinstance(perm, BasePermission):
            raise EnumMemberError(
                f'Parameter `perm` expected an {BasePermission} member or inherit, but other was given.'
            )
        self._perm = perm

        self._map = mapping or {}
        self._header = header or {}
        self._params = params or {}
        self._error_example = error_example or {}
        self._error_params = error_params or {}

        if success_example:
            self._success_example = SlightParam(success_example).slim
        else:
            self._success_example = {}

        if success_params:
            self._success_params = NestParam(success_params).single
        else:
            self._success_params = {}

    @property
    def doc(self) -> str:
        raw = self._func_statement() + '\n' + self._annotations()
        fmt = _lines_with_indent(raw)
        return fmt

    def _func_statement(self) -> str:
        parts = _parts_from_split(self._path)

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
        rows = _lines_from_join(check_parts)
        fmt = _lines_with_indent(rows)

        return fmt

    @staticmethod
    def _fmt_quotes() -> str:
        return '"""'

    def _fmt_declare(self) -> str:
        fmt = ApiDoc.Declare.statement(
            method=self._method,
            path=self._path,
            title=self._title,
        )
        return fmt

    def _fmt_description(self) -> str:
        fmt = ApiDoc.Desc.explain(content=self._desc)
        return fmt

    def _fmt_group(self) -> str:
        fmt = ApiDoc.Group.explain(content=self._group)
        return fmt

    def _fmt_permission(self) -> str:
        fmt = ApiDoc.Perm.instruction(
            permit=self._perm,
        )
        return fmt

    def _fmt_header(self) -> str:
        p = self._header
        fmt = _formatted_params(
            params=p,
            formatter=ApiDoc.Header,
            mapping=self._map,
            group=self._header_group,
        )
        return fmt

    def _fmt_header_eg(self) -> str:
        o = self._header
        fmt = _formatted_example(
            obj=o,
            formatter=ApiDoc.Header,
            group=self._header_group,
        )
        return fmt

    def _fmt_params(self) -> str:
        p = self._params
        fmt = _formatted_params(
            params=p,
            formatter=ApiDoc.Param,
            mapping=self._map,
            group=self._params_group,
        )
        return fmt

    def _fmt_params_eg(self) -> str:
        o = self._params
        fmt = _formatted_example(
            obj=o,
            formatter=ApiDoc.Param,
            group=self._params_group,
        )
        return fmt

    def _fmt_success(self) -> str:
        p = self._success_params
        fmt = _formatted_params(
            params=p,
            formatter=ApiDoc.Success,
            mapping=self._map,
            group=self._success_group,
        )
        return fmt

    def _fmt_success_eg(self) -> str:
        o = self._success_example
        fmt = _formatted_example(
            obj=o,
            formatter=ApiDoc.Success,
            group=self._success_group,
        )
        return fmt

    def _fmt_error(self) -> str:
        p = self._error_params
        fmt = _formatted_params(
            params=p,
            formatter=ApiDoc.Error,
            mapping=self._map,
            group=self._error_group,
        )
        return fmt

    def _fmt_error_eg(self) -> str:
        o = self._error_example
        fmt = _formatted_example(
            obj=o,
            formatter=ApiDoc.Error,
            group=self._error_group,
        )
        return fmt


class NotEnoughGroupsError(Exception):
    pass


class MulParamsFormatter(Formatter):
    """
    Using for multiple params.
    """

    def __init__(
            self,
            path: str,
            method: RequestMethod,
            title: str,
            group: Optional[str] = '',
            desc: Optional[str] = '',
            perm: Optional[BasePermission] = Permission.Nothing,
            mapping: Optional[Dict] = None,
            mul_groups: Optional[Sequence[str]] = None,
            mul_items: Optional[Sequence[Dict]] = None,
    ) -> None:
        super().__init__(
            path,
            method,
            title,
            group,
            desc,
            perm,
            mapping,
        )

        # groups should not less than examples.
        if mul_groups and mul_items and 0 < len(mul_groups) < len(mul_items):
            raise NotEnoughGroupsError(
                'Multiple groups should not less than multiple examples to escape `index error`.'
            )

        self._mul_groups = mul_groups
        self._mul_items = mul_items

        self.__set_mul_attrs()

    def __set_mul_attrs(self) -> None:
        item_names = [
            'header',
            'params',
            'success_params',
            'success_example',
            'error_params',
            'error_example',
        ]
        for key in item_names:
            setattr(self, f'_mul_{key}', self.__items_by_key(key))

        group_names = [
            'header',
            'params',
            'success',
            'error',
        ]
        for key in group_names:
            setattr(self, f'_mul_{key}_groups', self.__groups_for_key(key))

    def __items_by_key(
            self,
            key: str,
    ) -> List[Dict]:
        items = []
        for m in self._mul_items:
            i = m.get(key, {})
            items.append(i)

        return items

    def __groups_for_key(
            self,
            key: str,
    ) -> List[str]:
        """
        There are three levels group: <top: key-group> <mid: group> <bottom: basic-group>.
        If none group set, a key name with index will replace.
        """
        mul = self._mul_items

        if self._mul_groups:
            mul_groups = self._mul_groups
        else:
            mul_groups = [f'{key}-{i + 1}' for i in range(len(mul))]

        groups = []
        for i, m in enumerate(mul):
            g1 = m.get('header_group', '')
            g2 = m.get('group', '')
            g3 = mul_groups[i]

            g = g1 or g2 or g3
            groups.append(g)

        return groups

    def _annotations(self) -> str:
        parts = [
            self._fmt_quotes(),
            self._fmt_declare(),
            self._fmt_description(),
            self._fmt_group(),
            self._fmt_permission(),
        ]

        parts.extend(self._fmt_mul_header())
        parts.extend(self._fmt_mul_header_eg())

        parts.extend(self._fmt_mul_params())
        parts.extend(self._fmt_mul_params_eg())

        parts.extend(self._fmt_mul_success())
        parts.extend(self._fmt_mul_success_eg())

        parts.extend(self._fmt_mul_error())
        parts.extend(self._fmt_mul_error_eg())

        parts.append(self._fmt_quotes())

        check_parts = filter(lambda x: x, parts)
        rows = _lines_from_join(check_parts)
        fmt = _lines_with_indent(rows)

        return fmt

    def _fmt_mul_header(self) -> List[str]:
        mul = getattr(self, '_mul_header')
        groups = getattr(self, '_mul_header_groups')

        mul_fmts = []
        for i, p in enumerate(mul):
            fmt = _formatted_params(
                params=p,
                formatter=ApiDoc.Header,
                mapping=self._map,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_header_eg(self) -> List[str]:
        mul = getattr(self, '_mul_header')
        groups = getattr(self, '_mul_header_groups')

        mul_fmts = []
        for i, o in enumerate(mul):
            fmt = _formatted_example(
                obj=o,
                formatter=ApiDoc.Header,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_params(self) -> List[str]:
        mul = getattr(self, '_mul_params')
        groups = getattr(self, '_mul_params_groups')

        mul_fmts = []
        for i, p in enumerate(mul):
            fmt = _formatted_params(
                params=p,
                formatter=ApiDoc.Param,
                mapping=self._map,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_params_eg(self) -> List[str]:
        mul = getattr(self, '_mul_params')
        groups = getattr(self, '_mul_params_groups')

        mul_fmts = []
        for i, o in enumerate(mul):
            fmt = _formatted_example(
                obj=o,
                formatter=ApiDoc.Param,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_success(self) -> List[str]:
        mul = getattr(self, '_mul_success_params')
        groups = getattr(self, '_mul_success_groups')

        mul_fmts = []
        for i, p in enumerate(mul):
            fmt = _formatted_params(
                params=p,
                formatter=ApiDoc.Success,
                mapping=self._map,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_success_eg(self) -> List[str]:
        mul = getattr(self, '_mul_success_example')
        groups = getattr(self, '_mul_success_groups')

        mul_fmts = []
        for i, o in enumerate(mul):
            fmt = _formatted_example(
                obj=o,
                formatter=ApiDoc.Success,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_error(self) -> List[str]:
        mul = getattr(self, '_mul_error_params')
        groups = getattr(self, '_mul_error_groups')

        mul_fmts = []
        for i, p in enumerate(mul):
            fmt = _formatted_params(
                params=p,
                formatter=ApiDoc.Error,
                mapping=self._map,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts

    def _fmt_mul_error_eg(self) -> List[str]:
        mul = getattr(self, '_mul_error_example')
        groups = getattr(self, '_mul_error_groups')

        mul_fmts = []
        for i, o in enumerate(mul):
            fmt = _formatted_example(
                obj=o,
                formatter=ApiDoc.Error,
                group=groups[i],
            )
            mul_fmts.append(fmt)

        return mul_fmts
