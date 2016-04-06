# -*- encoding: utf-8 -*-
##################################################################################
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
##################################################################################

{
    'name': 'Base VAT Unique - To check Unique VAT number',
    'version': '8.0.1.0',
    'category': 'Base',
    'description': """
    Description
    ===========
    Dependencies
    ============
    - base_vat
    This module check the unique vat numbers to avoid duplicate vat numbers
    """,
    'author': 'jeo Software',
    'depends': ['base_vat'],
    "data": [
        "views/res_partner_view.xml",
    ],
    'website': 'http://jeo-soft.com.ar',
    'auto_install': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
