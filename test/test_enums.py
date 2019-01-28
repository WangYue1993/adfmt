#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest

from adfmt.enums import (
    RequestMethod,
    BasePermission,
    ParamTyping,
    ApiDoc,
)


class TestRequestMethod(unittest.TestCase):
    m = RequestMethod

    def test_get(self) -> None:
        m = self.m

        get = m.Get
        self.assertEqual(get.formatted, '{get}')

    def test_post(self) -> None:
        m = self.m

        post = m.Post
        self.assertEqual(post.formatted, '{post}')


class CustomPermission(BasePermission):
    Admin = 'User admin'
    Nothing = ''


class TestPermissionDerive(unittest.TestCase):
    p = CustomPermission

    def test_admin(self) -> None:
        p = self.p

        admin = p.Admin
        self.assertEqual(admin.explain, 'User admin')

    def test_nothing(self) -> None:
        p = self.p

        nothing = p.Nothing
        self.assertEqual(nothing.explain, '')


class TestParamTyping(unittest.TestCase):
    t = ParamTyping

    def test_str(self) -> None:
        t = self.t

        string = t.Str
        self.assertEqual(string.formatted, '{String}')

    def test_list(self) -> None:
        t = self.t

        array = t.List
        self.assertEqual(array.formatted, '{Array}')

    def test_num(self) -> None:
        t = self.t

        number = t.Num
        self.assertEqual(number.formatted, '{Number}')

    def test_obj(self) -> None:
        t = self.t

        obj = t.Obj
        self.assertEqual(obj.formatted, '{Object}')

    def test_bool(self) -> None:
        t = self.t

        boolean = t.Bool
        self.assertEqual(boolean.formatted, '{Boolean}')


class TestApiDoc(unittest.TestCase):
    a = ApiDoc

    def test_declare(self) -> None:
        a = self.a

        declare = a.Declare
        self.assertEqual(
            declare.statement(
                method=RequestMethod.Post,
                path='/test',
                title='test',
            ),
            '@api {post} /test test',
        )

    def test_permission(self) -> None:
        a = self.a

        perm = a.Perm
        self.assertEqual(
            perm.instruction(
                permit=CustomPermission.Admin,
            ),
            '@apiPermission admin User admin',
        )

    def test_group(self) -> None:
        a = self.a

        group = a.Group
        self.assertEqual(
            group.explain(
                content='test',
            ),
            '@apiGroup test',
        )

    def test_description(self) -> None:
        a = self.a

        desc = a.Desc
        self.assertEqual(
            desc.explain(
                content='test',
            ),
            '@apiDescription test',
        )

    def test_header(self) -> None:
        a = self.a

        header = a.Header
        self.assertEqual(
            header.param(
                typing=ParamTyping.Str,
                group='(test)',
                name='test',
                explain='param: test',
            ),
            '@apiHeader (test) {String} test param: test',
        )

        self.assertEqual(
            header.example(
                name='header-example',
                content=json.dumps(dict(test='test')),
            ),
            '@apiHeaderExample {json} header-example\n%s' % json.dumps(dict(test='test')),
        )

    def test_param(self) -> None:
        a = self.a

        param = a.Param
        self.assertEqual(
            param.param(
                typing=ParamTyping.Num,
                group='(test)',
                name='test',
                explain='param: test',
            ),
            '@apiParam (test) {Number} test param: test',
        )

        self.assertEqual(
            param.example(
                name='param-example',
                content=json.dumps(dict(test='test')),
            ),
            '@apiParamExample {json} param-example\n%s' % json.dumps(dict(test='test')),
        )

    def test_success(self) -> None:
        a = self.a

        success = a.Success
        self.assertEqual(
            success.param(
                typing=ParamTyping.Bool,
                group='(test)',
                name='test',
                explain='success: test',
            ),
            '@apiSuccess (test) {Boolean} test success: test',
        )

        self.assertEqual(
            success.example(
                name='success-example',
                content=json.dumps(dict(test='test')),
            ),
            '@apiSuccessExample {json} success-example\n%s' % json.dumps(dict(test='test')),
        )

    def test_error(self) -> None:
        a = self.a

        error = a.Error
        self.assertEqual(
            error.param(
                typing=ParamTyping.List,
                group='(test)',
                name='test',
                explain='error: test',
            ),
            '@apiError (test) {Array} test error: test',
        )

        self.assertEqual(
            error.example(
                name='error-example',
                content=json.dumps(dict(test='test')),
            ),
            '@apiErrorExample {json} error-example\n%s' % json.dumps(dict(test='test')),
        )


if __name__ == '__main__':
    unittest.main()
