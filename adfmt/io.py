#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def writing(
        filename: str,
        path: str,
        content: str,
) -> None:
    name = f'{filename}.py'
    target = os.path.join(path, name)

    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
