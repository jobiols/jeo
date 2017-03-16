# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
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
##############################################################################
{
    'name': 'Product Catalog Aeroo',
    'version': '8.0.1.0.0',
    'category': 'Aeroo Reporting',
    'sequence': 14,
    'summary': '',
    'description': """
Product Catalog Aeroo Report
============================
Lo mismo que el product_catalog_aeroo_report de ADHOC, pero con la diferencia
de que este no reporta los productos que:

- Tienen estado obsoleto
- No tienen el tilde de puede ser vendido


    """,
    'author': 'ADHOC SA, jeo Software',
    'website': 'www.jeosoft.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        # 'product',
        'product_price_taxes_included',
        'report_aeroo',
    ],
    'data': [
        'wizard/product_catalog_wizard.xml',
        'security/ir.model.access.csv',
        'product_catalog.xml',
        'report/product_catalog_view.xml'
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
