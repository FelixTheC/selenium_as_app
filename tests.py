#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""
from unittest import TestCase

from sql_alchemy_models import CredentialsModel


class ModelTests(TestCase):

    def setUp(self) -> None:
        pass
        # create new database

    def tearDown(self) -> None:
        pass
        # delete database

    def test_credential_model_create_without_errors(self):
        credent1 = CredentialsModel(username='test', password='abc123', login_url='/')
        self.assertIsNotNone(credent1)
        self.assertEqual('test', credent1.username)
        self.assertEqual('/', credent1.login_url)
        credent2 = CredentialsModel()
        credent2.username = 'test2'
        credent2.password = 'abc123'
        credent2.login_url = '/'
        credent2.save()
        self.assertIsNotNone(credent2)
        self.assertEqual('test2', credent2.username)
        self.assertNotEqual(credent1, credent2)

    def test_credential_create_fails(self):
        error = None
        try:
            CredentialsModel(username='test', password='abc123', login_url='/')
        except Exception as e:
            error = e
        self.assertIsNotNone(error)
        self.assertIsInstance(error, KeyError)

    def test_credential_login(self):
        credent = CredentialsModel().login('test', 'abc123')
        self.assertIsNotNone(credent)
        self.assertEqual('test', credent.username)

    def test_credential_logout(self):
        credent = CredentialsModel().login('test', 'abc123')
        credent.logout()
        self.assertIsNone(credent.username)
        self.assertIsNone(credent.password)
        self.assertIsNone(credent.login_url)
        self.assertEqual('', str(credent))
