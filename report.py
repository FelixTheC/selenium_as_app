#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""
import os
from datetime import datetime
import sys


class Report(object):

    def __init__(self, filepath):
        self.filepath = filepath
        if not self.__directory_exists():
            os.mkdir(self.filepath)
        self.__create_file__()

    def __directory_exists(self):
        return os.path.isdir(self.filepath)

    def __create_file__(self):
        self.report_file = os.path.join(self.filepath, f'report_{datetime.today().ctime()}.html')
        with open(self.report_file, 'w+') as file:
            file.write('<!DOCTYPE html >')
            file.write('\n')
            file.write('<html lang="en">')
            file.write('\n')
            file.write('<head>')
            file.write('\n')
            file.write('<meta charset="UTF-8">')
            file.write('\n')
            file.write('<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>')
            file.write('\n')
            file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>')
            file.write('\n')
            file.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.0/css/bootstrap.min.css" integrity="sha384-PDle/QlgIONtM1aqA2Qemk5gPOE7wFq8+Em+G/hmo5Iq0CCmYZLv3fVRDJ4MMwEA" crossorigin="anonymous" >')
            file.write('\n')

    def __finish_report(self):
        with open(self.report_file, 'a+') as file:
            file.write('\n')
            file.write('</html>')
