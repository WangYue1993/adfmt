#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In the beginning, all of enum members name were written in uppercase letters.

The reason for using uppercase letters which given on Python enum's doc is that make it easily to distinguish difference
between member of enumerations and method.

However, you may want to declare a name with rich expression sometime.

For example:
```
>>> # ver.1
>>> class Color(Enum):
...     RED = 1
...     GREEN = 2
...     BLUE = 3
>>>
>>> red = Color.RED
>>>
>>> # You may want add other colors.
>>> # And you should using uppercase.
>>> # ver.2
>>> class Color(Enum):
...     RED = 1
...     GREEN = 2
...     BLUE = 3
...     LIGHT_RED = 4   # it looks a little different
>>>
>>> light_red = Color.LIGHT_RED
```

The name of lightly red color is written by all uppercase words, it is similar to the convention of constant.
For Python Code Style Guide, I think it may be the reason why using uppercase is that
enum is very similar to constant and more safe than constant, so it should use the similar style guide with constant.

But, enum is enum, not constant.
We can easily distinguish name of enum class, constant and variable,
the only problem is that how we can make a difference between enum members and enum class' methods.

There are many ways to solve it, the simple way is using 'Pascal Case' but not 'Upper Case' for enum member name.

The 'Pascal Case' word has stronger readability than 'Upper Case' word.
eg: `ConstantConvention` vs `CONSTANT_CONVENTION`.

And I think it will reduce consuming of energy with typing code. :)
"""

from enum import Enum

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
    def format(self) -> str:
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
    def format(self) -> str:
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
            method.format,
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
    ) -> str:
        return '%sExample {json} %s-example\n%s' % (
            self.value,
            self.name.lower(),
            content,
        )

    def param(
            self,
            typing: ParamTyping,
            name: str,
            explain: str,
    ) -> str:
        f = [
            self.value,
            typing.format,
            name,
            explain,
        ]
        return ' '.join(f)
