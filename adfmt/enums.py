#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import (
    Enum,
)


class StrEnum(str, Enum):
    pass


class RequestMethod(StrEnum):
    GET = 'get'
    POST = 'post'

    @property
    def format(self) -> str:
        return '{%s}' % self.value


class BasePermission(StrEnum):
    """
    Instead of using a string-literal to represent permission, the enum-members are recommended.
    It was called 'hard-coding' for first way.
    """

    @property
    def explain(self) -> str:
        return self.value


class Permission(StrEnum):
    NONE = ''


class ParamTyping(StrEnum):
    STR = 'String'
    NUM = 'Number'
    BOOL = 'Boolean'
    OBJ = 'Object'
    LIST = 'Array'

    @property
    def format(self) -> str:
        return '{%s}' % self.value


class ApiDoc(StrEnum):
    # api
    DECLARE = '@api'

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
    PERM = '@apiPermission'

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
    GROUP = '@apiGroup'
    DESC = '@apiDescription'

    def explain(
            self,
            content: str,
    ) -> str:
        if content:
            return f'{self.value} {content}'
        else:
            return ''

    # params
    HEADER = '@apiHeader'
    PARAM = '@apiParam'
    SUCCESS = '@apiSuccess'
    ERROR = '@apiError'

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
