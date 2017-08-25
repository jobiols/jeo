# -*- encoding: utf-8 -*-
##################################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
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
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Description
===========
Este modulo chequea que el CUIT sea único, si no lo es no deja dar alta al partner generando
una excepción "El CUIT xx-xxxxxxxx-x ya está ingresado"

Dependencies
============
- base_vat

    """,
    'author': 'Cubic ERP, jeo Software',
    'depends': ['base_vat'],
    "data": [],
    'website': 'http://jeosoft.com.ar',
    'auto_install': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
