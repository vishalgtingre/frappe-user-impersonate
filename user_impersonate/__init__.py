# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'

from frappe import local
# -*- coding: utf-8 -*-

def init():
    local.session.isimpersonated = False
    local.session.impersonatedby = ''
