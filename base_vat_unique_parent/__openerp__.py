# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Base VAT Unique Parent',
    'version': '8.0.0.2',
    'category': 'Base',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
Descripción
===========
Los CUIT (VAT) deberán ser únicos para cada partner, solo podrán tener igual CUIT (VAT)
aquellos Partners que tengan una relación padre/hijo.
Al querer guardar un cliente con CUIT (VAT) existente se muestra una advertencia:
“ya existe un partner (nombre_partner) con ese número de CUIT. Para poder usar el mismo
CUIT (VAT) este partner debe ser hijo de (nombre_partner)”

Dependencias
============
- base
- base_vat

Observaciones
=============
No se modifican campos de objetos, solo hay que modificar sql_constraints del archivo
base_vat_unique.py para que valide de la manera que se detalla en la descripción.

    """,
    'author': 'jeo Software',
    'website': 'http://jeo-soft.com.ar',
    'depends': ['base', 'base_vat'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
