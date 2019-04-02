#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 02.04.19
@author: felix
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def main_url():
    return render_template('main.html')
