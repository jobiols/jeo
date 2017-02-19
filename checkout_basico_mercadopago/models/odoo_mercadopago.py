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
import logging
from openerp.exceptions import Warning

import mercadopago

_logger = logging.getLogger(__name__)

SHIPPING_METHODS = {'standard': 73328, 'priority': 73330}

TODO: Si el access token está mal da una horrible excepción, revisar y borrar el access token
TODO: Hacer que el boton de mercadopago aparezca solo cuando se pone el metodo de pago mercadopago.

class omp():
    def __init__(self, params):
        self._params = params
        # https://www.mercadopago.com.ar/developers/en/api-docs/basics/authentication/
        # traer el token de la configuración, si no existe lo creamos.
        access_token = params.get_param('mercadopago_access_token', default=False)
        if not access_token:
            client_id = params.get_param('mercadopago_client_id', default=False)
            client_secret = params.get_param('mercadopago_client_secret', default=False)
            if not client_id:
                params.set_param('mercadopago_client_id', 'your-client-id')
            if not client_secret:
                params.set_param('mercadopago_client_secret', 'your-client-secret')
            self._mp = mercadopago.MP(client_id, client_secret)
            params.set_param('mercadopago_access_token', self._mp.get_access_token())
            return
        # intentar crear el objeto _mp, si no se puede borramos de nuevo el token y avisamos
        # con una excepcion que hay que actualizar las credenciales.
        self._mp = mercadopago.MP(access_token)

    def shipping_methods(self, methods):
        ret = []
        for sm in methods:
            ret.append({'id': SHIPPING_METHODS.get(sm)})
        return ret

    def shipments(self, zip='5400', free_methods=[], dimensions="30x30x30,500",
                  default_sm='standard'):
        ret = {}
        ret['mode'] = 'me2'
        ret['dimensions'] = dimensions
        ret['local_pickup'] = True
        ret['free_methods'] = self.shipping_methods(free_methods)  # [ {"id": 73328} ]
        ret['default_shipping_method'] = SHIPPING_METHODS.get(default_sm)
        ret['zip_code'] = zip
        return ret

    def refund_pay(self, id):
        self._mp.refund_payment(':{}'.format(id))

    def pay_url(self, title, price):
        """ Genera la url del boton de pago
            https://www.mercadopago.com.ar/developers/en/solutions/payments/basic-checkout/receive-payments/
        """
        preference = {
            "items": [
                {
                    "title": title,
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": price,
                },
            ],
            #            "shipments": self.shipments()
        }

        preference_result = self._mp.create_preference(preference)
        if preference_result['status'] != 201:
            _logger.error('error')

        return preference_result["response"]

    def get_shipping_options(self):
        print self._mp.get('/shipping_options')

        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


{
    'status': 201,
    'response': {
        u'shipments': {
            u'receiver_address': {
                u'apartment': u'', u'street_name': u'', u'floor': u'',
                u'street_number': None, u'zip_code': u''}
        },
        u'auto_return': u'',
        u'marketplace': u'NONE',
        u'expires': False,
        u'expiration_date_to': None,
        u'external_reference': u'',
        u'payer': {u'surname': u'',
                   u'name': u'',
                   u'phone': {u'area_code': u'', u'number': u''},
                   u'identification': {u'type': u'', u'number': u''},
                   u'address': {u'street_name': u'', u'street_number': None,
                                u'zip_code': u''},
                   u'date_created': u'',
                   u'email': u''
                   },
        u'items': [
            {
                u'description': u'',
                u'title': u'curso de automaquillaje',
                u'picture_url': u'',
                u'unit_price': 110,
                u'currency_id': u'ARS',
                u'category_id': u'',
                u'id': u'',
                u'quantity': 1}
        ],
        u'id': u'142827273-7016ddce-8c5d-4077-9b5c-353f8a41f764',
        u'notification_url': None,
        u'expiration_date_from': None,
        u'payment_methods': {
            u'installments': None,
            u'excluded_payment_types': [{u'id': u''}],
            u'default_installments': None,
            u'default_payment_method_id': None,
            u'excluded_payment_methods': [{u'id': u''}]
        },
        u'back_urls': {u'failure': u'', u'pending': u'', u'success': u''},
        u'init_point': u'https://www.mercadopago.com/mla/checkout/start?pref_id=142827273-7016ddce-8c5d-4077-9b5c-353f8a41f764',
        u'collector_id': 142827273, u'client_id': u'963',
        u'sandbox_init_point': u'https://sandbox.mercadopago.com/mla/checkout/pay?pref_id=142827273-7016ddce-8c5d-4077-9b5c-353f8a41f764',
        u'operation_type': u'regular_payment',
        u'date_created': u'2016-11-03T18:22:16.532-04:00',
        u'marketplace_fee': 0,
        u'additional_info': u''}
}
