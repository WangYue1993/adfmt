#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from adfmt.enums import (
    RequestMethod,
    BasePermission,
    ParamTyping,
    ApiDoc,
)


def test_request_method() -> None:
    get = RequestMethod.GET
    assert get.format == '{get}'

    post = RequestMethod.POST
    assert post.format == '{post}'


class CustomPermission(BasePermission):
    ADMIN = 'User admin'
    NONE = ''


def test_inherit_permission() -> None:
    admin = CustomPermission.ADMIN
    assert admin.explain == 'User admin'

    none = CustomPermission.NONE
    assert none.explain == ''


def test_param_typing() -> None:
    string = ParamTyping.STR
    assert string.format == '{String}'

    array = ParamTyping.LIST
    assert array.format == '{Array}'

    number = ParamTyping.NUM
    assert number.format == '{Number}'

    obj = ParamTyping.OBJ
    assert obj.format == '{Object}'

    boolean = ParamTyping.BOOL
    assert boolean.format == '{Boolean}'


def test_api_doc() -> None:
    declare = ApiDoc.DECLARE
    assert declare.statement(
        method=RequestMethod.POST,
        path='/test',
        title='test',
    ) == '@api {post} /test test'

    perm = ApiDoc.PERM
    assert perm.instruction(
        permit=CustomPermission.ADMIN,
    ) == '@apiPermission admin User admin'

    group = ApiDoc.GROUP
    assert group.explain(
        content='test',
    ) == '@apiGroup test'

    desc = ApiDoc.DESC
    assert desc.explain(
        content='test',
    ) == '@apiDescription test'

    header = ApiDoc.HEADER
    assert header.param(
        typing=ParamTyping.STR,
        name='test',
        explain='param: test',
    ) == '@apiHeader {String} test param: test'
    assert header.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiHeaderExample {json} header-example\n%s' % json.dumps(dict(test='test'))

    param = ApiDoc.PARAM
    assert param.param(
        typing=ParamTyping.NUM,
        name='test',
        explain='param: test',
    ) == '@apiParam {Number} test param: test'
    assert param.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiParamExample {json} param-example\n%s' % json.dumps(dict(test='test'))

    success = ApiDoc.SUCCESS
    assert success.param(
        typing=ParamTyping.BOOL,
        name='test',
        explain='success: test',
    ) == '@apiSuccess {Boolean} test success: test'
    assert success.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiSuccessExample {json} success-example\n%s' % json.dumps(dict(test='test'))

    error = ApiDoc.ERROR
    assert error.param(
        typing=ParamTyping.LIST,
        name='test',
        explain='error: test',
    ) == '@apiError {Array} test error: test'
    assert error.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiErrorExample {json} error-example\n%s' % json.dumps(dict(test='test'))


if __name__ == '__main__':
    test_request_method()
    test_inherit_permission()
    test_param_typing()
    test_api_doc()
