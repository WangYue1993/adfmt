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
    get = RequestMethod.Get
    assert get.format == '{get}'

    post = RequestMethod.Post
    assert post.format == '{post}'


class CustomPermission(BasePermission):
    Admin = 'User admin'
    Nothing = ''


def test_inherit_permission() -> None:
    admin = CustomPermission.Admin
    assert admin.explain == 'User admin'

    none = CustomPermission.Nothing
    assert none.explain == ''


def test_param_typing() -> None:
    string = ParamTyping.Str
    assert string.format == '{String}'

    array = ParamTyping.List
    assert array.format == '{Array}'

    number = ParamTyping.Num
    assert number.format == '{Number}'

    obj = ParamTyping.Obj
    assert obj.format == '{Object}'

    boolean = ParamTyping.Bool
    assert boolean.format == '{Boolean}'


def test_api_doc() -> None:
    declare = ApiDoc.Declare
    assert declare.statement(
        method=RequestMethod.Post,
        path='/test',
        title='test',
    ) == '@api {post} /test test'

    perm = ApiDoc.Perm
    assert perm.instruction(
        permit=CustomPermission.Admin,
    ) == '@apiPermission admin User admin'

    group = ApiDoc.Group
    assert group.explain(
        content='test',
    ) == '@apiGroup test'

    desc = ApiDoc.Desc
    assert desc.explain(
        content='test',
    ) == '@apiDescription test'

    header = ApiDoc.Header
    assert header.param(
        typing=ParamTyping.Str,
        name='test',
        explain='param: test',
    ) == '@apiHeader {String} test param: test'
    assert header.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiHeaderExample {json} header-example\n%s' % json.dumps(dict(test='test'))

    param = ApiDoc.Param
    assert param.param(
        typing=ParamTyping.Num,
        name='test',
        explain='param: test',
    ) == '@apiParam {Number} test param: test'
    assert param.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiParamExample {json} param-example\n%s' % json.dumps(dict(test='test'))

    success = ApiDoc.Success
    assert success.param(
        typing=ParamTyping.Bool,
        name='test',
        explain='success: test',
    ) == '@apiSuccess {Boolean} test success: test'
    assert success.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiSuccessExample {json} success-example\n%s' % json.dumps(dict(test='test'))

    error = ApiDoc.Error
    assert error.param(
        typing=ParamTyping.List,
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
