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
from openerp import models, fields, api
from odoo_mercadopago import omp
import logging
_logger = logging.getLogger(__name__)

class account_voucher(models.Model):
    _inherit = "account.voucher"
    mercadopago_id = fields.Char()

    @api.multi
    def button_refund_mercadopago(self):
        print 'button refund-------------------'
        for rec in self:
            om = omp()
            _logger.info('vamos a devolverle el pago a {}'.format(rec.partner_id.name))
            print 'refund--------------------> ',om.refund_pay(rec.mercadopago_id)

    @api.multi
    def button_pay_mercadopago(self):
        for rec in self:
            print rec.partner_id.name
            print rec.amount
            om = omp()
            _logger.info('{} va a pagar ${}'.format(rec.partner_id.name,rec.amount))
            resp = om.pay_url(rec.partner_id.name,rec.amount)
#            url = resp["sandbox_init_point"]
            url = resp["init_point"]
            rec.mercadopago_id = resp['id']
            return {
                    'type': 'ir.actions.act_url',
                    'url': url,
                    'target': 'new'
            }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: