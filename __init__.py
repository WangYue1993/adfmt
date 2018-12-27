#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = "adfmt"

from adfmt.format import (
    Formatter,
    format_class,
)

from adfmt.io import (
    writing,
)

writing_api_doc = writing

__all__ = [
    'Formatter',
    'format_class',
    'writing_api_doc',
]
