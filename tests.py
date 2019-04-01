#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""
from unittest import TestCase
import os

from report import Report
from sql_alchemy_models import CredentialsModel, TestUrlsModel, ModelBase, TestObjectsModel


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

    def test_get_all_objs(self):
        turls = TestUrlsModel().all()
        self.assertTrue(len(turls) > 1)

    def test_filter_objs(self):
        turls = TestObjectsModel().filter(url_id=1)
        self.assertTrue(len(turls) > 0)
        for turl in turls:
            self.assertTrue(turl.url_id == 1)


class ReportTest(TestCase):
    filepath = 'tmp/'

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        for root, dir, files in os.walk(self.filepath):
            for file in files:
                os.remove(os.path.join(root, file))
        os.removedirs(self.filepath)

    def test_create_directory_during_init(self):
        report = Report(self.filepath)
        self.assertTrue(os.path.isdir(self.filepath))

    def test_report_file_was_created(self):
        report = Report(self.filepath)
        self.assertIsNotNone(report.report_file)
        with open(report.report_file, 'r+') as file:
            self.assertEqual('<!DOCTYPE html>', file.readline().strip())
            self.assertEqual('<html lang="en">', file.readline().strip())
            self.assertEqual('<head>', file.readline().strip())
            self.assertEqual('<meta charset="UTF-8">', file.readline().strip())
