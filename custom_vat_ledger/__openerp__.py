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
    'name': 'Custom Vat Ledger',
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Customiza el libro de IVA',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Customiza las columnas del libro de IVA (valente)
=================================================

**Fecha**
Fecha de la factura

**Comprobante**
Numero de comprobante comienza con el tipo de documento 4 caracteres, punto de venta
4 caracteres y nro de factura 8 caracteres. XX-X 0000-00000000

**Nombre**
Nombre del partner

**CUIT**
Cuit del partner con guiones

**Base**
Suma de las bases imponibles de todos los IVAs grabados (no cero)

**IVA 10.5%**
suma de todos los iva de los productos con IVA 10.5%

**IVA 21%**
suma de todos los iva de los productos con IVA 21%

**IVA 27%**
suma de todos los iva de los productos con IVA 27%

**No Gravado**
Total a pagar menos todos los demás items

**Perc IIBB**
Suma de todas las percepciones de IIBB

**Perc IVA**
Suma de todas las percepciones de IVA

**Total**
Total a pagar
""",
    'author': 'jeo software',
    'depends': ['sale', 'l10n_ar_account_vat_ledger'],
    'data': [
        'views/vat_ledger.xml'
    ],
    'test': [
        'tests/test_ledger.py'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
