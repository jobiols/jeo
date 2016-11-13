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
==========================

Este módulo permite importar una lista de precios desde un archivo que puede ser csv
o xls, el archivo tiene que tener las siguientes columnas.

Formato del archivo de importación
----------------------------------
**Columnas:** product_code, product_name, list_price, [package_qty,] [package_uom,] categ, sub_categ,
dp, dc1, dc2, ds1, ds2, ds3

Nota:las que estan entre corchetes son opcionales las seis últimas columnas definen su
comportamiento con los dos primeros caracteres del nombre.

**product_code** Es el código del producto, debe ser único y si no lo es odoo generará una
excepción, Esto lo maneja el módulo product_unique_default_code que esta como dependencia.

**product_name** Es el nombre del producto

**list_price** Es el precio de lista del proveedor, el precio al que el proveedor nos sugiere
vender al público, sobre este precio el proveedor nos hace una serie de descuentos.

**package_qty** *Opcional* Indica la cantidad de producto que hay en una caja sirve para aclarar en
la factura la cantidad total de producto que se vende dada la cantida de cajas vendidas.

**package_uom** *Opcional* Indica la unidad de medida del producto que está en la caja.

Las últimas seis columnas son los descuentos, los dos primeros caracteres del nombre de estas
columnas indican donde va a aplicarse el descuento.
- dp = descuento en el producto
- dc = descuent en la categoría
- ds = descuento en la sub categoría

En el ejemplo se pusieron dos descuentos para la categoría y tres para la sub categoría
pero se puede cambiar por ejemplo: dc1, ds1, ds2, ds3, ds4 en este caso tendríamos un
descuento para la categoría y cuatro para la sub categoría. El resto del nombre puede ser
cualquier cosa, se estila poner un número que sería el orden de las columnas.

Configuración
-------------
**Proveedores** Cada proveedor que va a enviar una lista de precios debe tener cargada
una categoría, esa categoría representa todos los productos del proveedor. Se estila ponerle
un nombre que tenga que ver con el nombre del proveedor en cuestion.



Forma de Uso
------------

Al importar se debe seleccionar el nombre del proveedor y definir si se agregan productos
o solo se actualizan los que ya están. El proveedor tiene que tener cargada una categoría
que lo represente usualmente con el mismo nombre o un nombre corto que lo identifique.

A cada categoria asignada a los proveedores se le pueden agregar descuentos, en la forma
de un número entre 0 y 100 y una descripción meramente informativa.
La cantidad de descuentos es ilimitada

""",
    'author': 'jeo Software',
    'website': 'http://www.jeo-soft.com.ar',
    'depends': ['purchase',
                'product_unique_default_code'],
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