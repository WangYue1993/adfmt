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
    assert get == 'get'
    assert get.name == 'GET'
    assert get.value == 'get'
    assert get.format == '{get}'

    post = RequestMethod.POST
    assert post == 'post'
    assert post.name == 'POST'
    assert post.value == 'post'
    assert post.format == '{post}'


class CustomPermission(BasePermission):
    ADMIN = 'User admin'
    NONE = ''


def test_inherit_permission() -> None:
    admin = CustomPermission.ADMIN
    assert admin == 'User admin'
    assert admin.name == 'ADMIN'
    assert admin.value == 'User admin'
    assert admin.explain == 'User admin'

    none = CustomPermission.NONE
    assert none == ''
    assert none.name == 'NONE'
    assert none.value == ''
    assert none.explain == ''


def test_param_typing() -> None:
    string = ParamTyping.STR
    assert string == 'String'
    assert string.name == 'STR'
    assert string.value == 'String'
    assert string.format == '{String}'

    array = ParamTyping.LIST
    assert array == 'Array'
    assert array.name == 'LIST'
    assert array.value == 'Array'
    assert array.format == '{Array}'

    number = ParamTyping.NUM
    assert number == 'Number'
    assert number.name == 'NUM'
    assert number.value == 'Number'
    assert number.format == '{Number}'

    obj = ParamTyping.OBJ
    assert obj == 'Object'
    assert obj.name == 'OBJ'
    assert obj.value == 'Object'
    assert obj.format == '{Object}'

    boolean = ParamTyping.BOOL
    assert boolean == 'Boolean'
    assert boolean.name == 'BOOL'
    assert boolean.value == 'Boolean'
    assert boolean.format == '{Boolean}'


def test_api_doc() -> None:
    declare = ApiDoc.DECLARE
    assert declare == '@api'
    assert declare.name == 'DECLARE'
    assert declare.value == '@api'
    assert declare.statement(
        method=RequestMethod.POST,
        path='/test',
        title='test',
    ) == '@api {post} /test test'

    perm = ApiDoc.PERM
    assert perm == '@apiPermission'
    assert perm.name == 'PERM'
    assert perm.value == '@apiPermission'
    assert perm.instruction(
        permit=CustomPermission.ADMIN,
    ) == '@apiPermission admin User admin'

    group = ApiDoc.GROUP
    assert group == '@apiGroup'
    assert group.name == 'GROUP'
    assert group.value == '@apiGroup'
    assert group.explain(
        content='test',
    ) == '@apiGroup test'

    desc = ApiDoc.DESC
    assert desc == '@apiDescription'
    assert desc.name == 'DESC'
    assert desc.value == '@apiDescription'
    assert desc.explain(
        content='test',
    ) == '@apiDescription test'

    header = ApiDoc.HEADER
    assert header == '@apiHeader'
    assert header.name == 'HEADER'
    assert header.value == '@apiHeader'
    assert header.param(
        typing=ParamTyping.STR,
        name='test',
        explain='param: test',
    ) == '@apiHeader {String} test param: test'
    assert header.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiHeaderExample {json} header-example\n%s' % json.dumps(dict(test='test'))

    param = ApiDoc.PARAM
    assert param == '@apiParam'
    assert param.name == 'PARAM'
    assert param.value == '@apiParam'
    assert param.param(
        typing=ParamTyping.NUM,
        name='test',
        explain='param: test',
    ) == '@apiParam {Number} test param: test'
    assert param.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiParamExample {json} param-example\n%s' % json.dumps(dict(test='test'))

    success = ApiDoc.SUCCESS
    assert success == '@apiSuccess'
    assert success.name == 'SUCCESS'
    assert success.value == '@apiSuccess'
    assert success.param(
        typing=ParamTyping.BOOL,
        name='test',
        explain='success: test',
    ) == '@apiSuccess {Boolean} test success: test'
    assert success.example(
        content=json.dumps(dict(test='test')),
    ) == '@apiSuccessExample {json} success-example\n%s' % json.dumps(dict(test='test'))

    error = ApiDoc.ERROR
    assert error == '@apiError'
    assert error.name == 'ERROR'
    assert error.value == '@apiError'
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
