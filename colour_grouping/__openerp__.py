# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------
{
    'name': 'Colour grouping',
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Colour grouping',
    'description': """

Colour grouping
===============
Groups registers by colour
""",
    'author': 'jeo software',
    'depends': [
        'base',
        'account',
        'web',
    ],
    'data': [
        'views/account_journal_view.xml',
        'views/res_partner_view.xml',
        'views/ribbon_view.xml',
        'views/res_users_view.xml',
        'data/colour_data.xml',
        'data/ribbon_data.xml',
        'security/ir.model.access.csv',
        'security/rules.xml'
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
