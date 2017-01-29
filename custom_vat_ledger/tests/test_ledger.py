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
from openerp.tests.common import SingleTransactionCase

# testear con
# ./odooenv.py -T jeo test_ledger.py -c valente -d valente_test -m custom_vat_ledger
#

class TestLedger(SingleTransactionCase):
    def setUp(self):
        super(TestLedger, self).setUp()
        self.partner_obj = self.env['res.partner']
        self.product_obj = self.env['product.product']
        self.invoice_obj = self.env['account.invoice']
        self.invoice_line_obj = self.env['account.invoice.line']

        print 'cargando datos ---'
        self.partner_1 = self.partner_obj.create(
            {'name': 'cliente 1',
             'responsability_id': 1,
             'customer': True
             }
        )

        self.product_1 = self.product_obj.create(
            {
                'name': 'producto 1',
                'type': 'product',
                'lst_price': 100

            }
        )

        invoice_lines = {
            'name': 'nombre de la linea',
            'sequence': 5,
            'invoice_id': False,
            'account_id': 177,  # venta de mercaderias
            #            'account_analytic_id': 4,
            'price_unit': 100,
            'quantity': 1.0,
        }
    """
        self.invoice_1 = self.invoice_obj.create(
            {
                'partner_id': self.partner_1.id,
                'invoice_line': [
                    (6, 0, [self.invoice_line_obj.create(invoice_lines).id])],
                'name': 'nombre',
                'type': 'out_invoice',
                'account_id': 8,
                'journal_id': 18,
                'currency_id': 20,
                'company_id': 1,
                'user_id': 1
            }
        )
    """

    def test_01(self):
        print 'test ledger 1 ----------------------------------'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
