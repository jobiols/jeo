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

.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Simplifica la facturación estilo TPV
====================================

En el formulario de presupuesto/orden de venta ademas de los botones standard aparecen
tres botones **Ent**, **Fac/Ent** y **Fac/Cob/Ent**:

Ent (Entrega)
-------------

- Verifica que solo haya productos, no servicios ni consumibles
- Confirma orden de venta
- Fuerza la asignación de materiales, si no hay stock los mueve igual
- Hace la transferencia de stock
- Genera el remito y lo baja en pdf

Fac/Ent (Facturación y Entrega)
-------------------------------

- Verifica que solo haya productos, no servicios ni consumibles
- Confirma orden de venta
- Fuerza la asignación de materiales, si no hay stock los mueve igual
- Hace la transferencia de stock

- Crea la factura
- Valida la factura

Fac/Cob/Ent (Facturación Cobro y Entrega)
-----------------------------------------

- Verifica que solo haya productos, no servicios ni consumibles
- Confirma orden de venta
- Fuerza la asignación de materiales, si no hay stock los mueve igual
- Hace la transferencia de stock

- Crea la factura
- Valida la factura

- Paga la factura usando metodo de pago Caja, (debe existir un diario 'Caja', y un formulario de recibos 'Recibos', los busca con un like)
- Concilia el pago con la factura
- Genera la factura y la baja en pdf, usa el documento por defecto.
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
