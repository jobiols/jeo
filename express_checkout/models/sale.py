# -*- coding: utf-8 -*-
################################################################################
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
################################################################################
from openerp import models, fields, exceptions, api, _

class sale_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def button_invoice_express(self):
        print '---------------------------- button_invoice_express'

        print '>> confirmar orden de venta'
        self.action_button_confirm()

        print '>> crear factura'
        res = self.manual_invoice()

        print 'validar factura -->',res['res_id']
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.browse([res['res_id']])
        invoice.invoice_validate()

        print 'pagar factura---------------------------------------------------'
        invoice.invoice_pay_customer()

        print 'imprimir factura'
        datas = {
                'ids': invoice.ids,
                'model': 'account.report_invoice',
                'form': invoice.read()
            }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.report_invoice',
            'datas': datas,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
