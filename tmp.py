#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""
from sql_alchemy_models import CredentialsModel, TestObjectsModel

if __name__ == '__main__':
    credent = CredentialsModel()
    credent.login('test_2', 'abc1234')
    print(credent.username == 'test_2')
    credent.logout()
    print((credent.username is not None) is False)
