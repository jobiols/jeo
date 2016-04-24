# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    'name': 'Product Pricelist Import',
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Importa lista de precios y crea productos',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
Importar listas de precios
--------------------------

Este módulo permite importar una lista de precios desde un archivo que puede ser csv
o xls, el archivo tiene que tener las siguientes columnas:

product_code, product_name, list_price, categ, sub_categ, dp, dc1, dc2, ds1, ds2, ds3

Las últimas seis lineas son los descuentos,
- dp = descuento en el producto
- dc = descuent en la categoría
- ds = descuento en la sub categoría

En el ejemplo se pusieron dos descuentos para la categoría y tres para la sub categoría
pero se puede cambiar por ejemplo: dc1, ds1, ds2, ds3, ds4 en este caso tendríamos un
descuento para la categoría y cuatro para la sub categoría.

Al importar se debe seleccionar el nombre del proveedor y definir si se agregan productos
o solo se actualizan los que ya están. El proveedor tiene que tener cargada una categoría
que lo representa.

""",
    'author': 'jeo Software',
    'website': 'http://www.jeo-soft.com.ar',
    'depends': ['purchase'],
    'data': ['wizard/import_price_file_view.xml',
             'views/product_pricelist_load_line_view.xml',
             'views/product_pricelist_load_view.xml',
             'views/product_category_view.xml',
             'views/product_supplierinfo_view.xml',
             'views/product_view.xml',
             'views/partner.xml',
             'security/ir.model.access.csv',
             'security/security_groups.xml'
             ],
    'test': [
        'tests/test_import.yml'
    ],
    'installable': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: