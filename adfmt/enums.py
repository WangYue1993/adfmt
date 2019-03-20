#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In the beginning, all of enum members name were written in uppercase letters.

For Python Code Style Guide, it may be the reason why using uppercase:
enum is very similar to constant and more safe,
so it should use the similar style guide with constant.

However, enum is enum, not constant.
the problem for enum member is that how we can make a difference between enum members and enum class methods.

There are many ways to solve it, the simple way is using 'Pascal Case' but not 'Upper Case'.

The 'Pascal Case' word has a stronger readability than 'Upper Case' word.
eg: `ConstantConventionReadabilityIsWorse` vs `CONSTANT_CONVENTION_READABILITY_IS_WORSE`.

Sometime if enum members and constant both use uppercase to declare, it's hard to distinguish them.

eg:
```color.py
RED = 1
BLUE = 2
GREEN = 3
```

```subject.py
import color
from enum import Enum

class Subject(Enum):
    MATH = 1
    ENG = 2
    ART = 3


def location_red_math():
    s = Subject.MATH.value

    # When you take constant as enum, a mistake will occur below called.
    c = color.RED.value

    return s * c
```
"""

from enum import Enum

from typing import Optional

__all__ = [
    'RequestMethod',
    'BasePermission',
    'Permission',
    'ParamTyping',
    'ApiDoc',
]


class _StrEnum(str, Enum):
    pass


class RequestMethod(_StrEnum):
    Get = 'get'
    Post = 'post'

    @property
    def formatted(self) -> str:
        return '{%s}' % self.value


class BasePermission(_StrEnum):
    """
    Instead of using a string-literal to represent permission, the enum-members are recommended.
    It was called 'hard-coding' for first way.
    """

    @property
    def explain(self) -> str:
        return self.value


class Permission(BasePermission):
    Nothing = ''
    Admin = 'User admin is required'


class ParamTyping(_StrEnum):
    Str = 'String'
    Num = 'Number'
    Bool = 'Boolean'
    Obj = 'Object'
    List = 'Array'

    @property
    def formatted(self) -> str:
        return '{%s}' % self.value


class ApiDoc(_StrEnum):
    # api
    Declare = '@api'

    def statement(
            self,
            method: RequestMethod,
            path: str,
            title: str,
    ) -> str:
        f = [
            self.value,
            method.formatted,
            path,
            title,
        ]
        return ' '.join(f)

    # permission
    Perm = '@apiPermission'

    def instruction(
            self,
            permit: BasePermission,
    ) -> str:
        f = [
            self.value,
            permit.name.lower(),
            permit.explain,
        ]
        return ' '.join(f)

    # explain
    Group = '@apiGroup'
    Desc = '@apiDescription'

    def explain(
            self,
            content: str,
    ) -> str:
        if content:
            return f'{self.value} {content}'
        else:
            return ''

    # params
    Header = '@apiHeader'
    Param = '@apiParam'
    Success = '@apiSuccess'
    Error = '@apiError'

    def example(
            self,
            content: str,
            name: str,
    ) -> str:
        return '%sExample {json} %s\n%s' % (
            self.value,
            name,
            content,
        )

    def param(
            self,
            typing: ParamTyping,
            name: str,
            explain: str,
            group: str,
    ) -> str:
        f = [
            self.value,
            group,
            typing.formatted,
            name,
            explain,
        ]

        return ' '.join(f)
