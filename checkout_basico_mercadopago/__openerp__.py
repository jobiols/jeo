# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------

{
    'name': 'Checkout básico mercadopago',
    'version': '8.0.0.0',
    'category': 'Tools',
    'summary': 'gateway hacia mercadopago',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Este modulo está en desarrollo y todavia no ha sido liberado

Checkout Básico Mercadopago
===========================
Implementa el checkout tal como se describe en la página de mercadopago
(https://www.mercadopago.com.ar/developers/es/solutions/payments/basic-checkout/receive-payments/)

Recibir pagos
-------------
En pagos de cliente si se elije un metodo de pago marcado como tarjeta al lado del
importe aparece el botón [Cobrar]. Oprimiendo cobrar lanza un popup con el sitio de
mercadopago y permite cobrar con tarjeta.

Utilizar mercadoenvios
----------------------
Si tiene activado mercadoenvios, en la orden de venta aparece un botón [Mercadoenvios]
en el producto debe estar definido el peso y las dimensiones para que se le transmitan
a mercadoenvios

Devoluciones y cancelaciones
----------------------------
No implementado

Recibir notificaciones de las operaciones
-----------------------------------------
No implementado
Requiere una url donde mercadopago postea las notificaciones.

""",
    'author': 'jeo Software',
    'website': 'http://www.jeo-soft.com.ar',
    'depends': [
        'sale'
    ],
    'data': [
        'views/account_voucher_view.xml'
#        'views/res_config_view.xml' // no lo pude hacer andar
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
