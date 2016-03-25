# -*- coding: utf-8 -*-
# ####################################################################################
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
# ###################################################################################
{
    'name': 'Express Checkout',
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Facturación simplificada',
    'description': """
Simplifica la facturación estilo TPV
====================================
En el formulario de presupuesto ademas de los botones standard aparece un boton
Facturar y Enviar que hace el movimiento de stock y luego genera una factura


""",
    'author': 'jeo software',
    'depends': ['sale'],
    'data': [
        'views/sale_view.xml'
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
