#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 02.04.19
@author: felix
"""
from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)


def render_with_navbar(template_name, **kwargs):
    urls = {'overview': url_for('overview'),
            'add_tasks': url_for('add_tasks'),
            }
    return render_template(template_name, urls=urls, **kwargs)


@app.route('/')
def main_url():
    return render_with_navbar('main.html')


@app.route('/overview', methods=['GET'])
def overview():
    pass


@app.route('/add_tasks', methods=['GET', 'POST'])
def add_tasks():
    return render_with_navbar('add_tasks.html')
