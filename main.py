#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 02.04.19
@author: felix
"""


def selenium_app_start():
    while True:
        if input('Quit with q:').lower() == 'q':
            break


if __name__ == '__main__':
    selenium_app_start()
