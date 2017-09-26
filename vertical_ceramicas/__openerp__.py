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
    'name': 'Vertical Ceramicas',
    'version': '8.0.1.1',
    'category': 'Tools',
    'summary': 'Customización mayorista de ceramicas',
    'description': """

Customización mayorista de ceramicas
====================================

# Definicion de cuatro grupos de usuarios
- Administrador
- Encargado
- Comercial
- Almacen

- parametro adicional m2 o m por caja en producto
- Si se usan descuentos, el Comercial solo pueden poner descuentos hasta 10%
- listas de precios restringidas, solo las ven Administrador y Encargado
- Definicion de rutas para envios desde cualquier sucursal
- Definicion de remitos para envios o para retiro en sucursal
- Definicion de tres columnas configurables en listado de productos para mostrar listas de precio


""",
    'author': 'jeo Software',
    'depends': [
        'product',
        'base',
        'base_multi_store',
        'stock_multi_store',
        'account',
        'stock',
        'purchase',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/account_tax_view.xml',
        'views/sale_view.xml',
        'views/pricelist_view.xml',
        'stock_report.xml',
        'views/report_stockpicking.xml',
        'views/res_company.xml',
        'views/account_invoice.xml',
        'views/res_config_view.xml',
        'views/res_product.xml',
    ],
    'test': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
