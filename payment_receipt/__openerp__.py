# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2017  jeo Software  (http://www.jeosoft.com.ar)
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
    "name": "Payment receipt",
    "version": "8.0.1.0",
    "author": "jeo Software",
    'website': 'http://www.jeosoft.com.ar',
    "depends": ["l10n_ar_base"],
    "category": "Generic Modules",
    "description": """
Imprime un recibo con las lineas de factura, el pago parcial (seña) y el total adeudado.
""",
    "demo_xml": [],
    "data": [
        'views/report_invoice_receipt.xml',
        'payment_receipt_report.xml'
    ],
    'depends': ['account'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
