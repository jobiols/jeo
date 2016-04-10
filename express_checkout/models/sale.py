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

    #    @api.multi
    #    def button_express(self):
    #        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> button_invoice_express'
    #        print 'quie paasa'
    #        print '>> confirmar orden de venta'
    #        self.action_button_confirm()

    #        print '--------------------------------------------------------- mover materiales'
    #        picking_obj = self.env['stock.picking']
    #        for rec in picking_obj.browse(self.ids):
    #            rec.force_assign()
    #            rec.do_transfer()

    @api.multi
    def button_invoice_express(self):
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> button invoice express'

        print '------------------------------------------------- confirmar orden de venta'
        self.action_button_confirm()

        print '------------------------------------------------------------ crear factura'
        res = self.manual_invoice()

        print '---------------------------------------------------------- validar factura'
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.browse([res['res_id']])
        invoice.signal_workflow('invoice_open')

        print '------------------------------------------------------------ pagar factura'
        res = invoice.invoice_pay_customer()
        context = res['context']
        account_voucher_obj = self.env['account.voucher']

        # hacer configuración para modificar esto.
        journal_obj = self.env['account.journal']
        journal = journal_obj.search([('name','like','Caja')],limit=1)
        partner = self.env['res.partner'].browse(context['default_partner_id'])

        # hacer configuracion para modificar esto
        receipt_obj = self.env['account.voucher.receiptbook']
        receipt = receipt_obj.search([('name','like','Recibos')],limit=1)

        voucher = account_voucher_obj.create({
                'partner_id':context['default_partner_id'],
                'journal_id':journal.id,
                'account_id':partner.property_account_receivable.id,
                'type':context['type'],
                'amount':context['default_amount'],
                'net_amount':context['default_amount'],
                'receiptbook_id': receipt.id
        })
        voucher.signal_workflow('proforma_voucher')

        print '--------------------------------------------------------- mover materiales'
        picking_obj = self.env['stock.picking']
        for rec in picking_obj.browse(self.ids):
            print 'force assign', rec.force_assign()
            print 'do transfer', rec.do_transfer()

        print '--------------------------------------------------------- imprimir factura'
        datas = {
                'ids': invoice.ids,
                'model': 'account.report_invoice',
                'form': invoice.read()
            }
        # print 'datas',datas
        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< button invoice express'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'l10n_ar_aeroo_einvoice.action_aeroo_report_ar_einvoice',
            'datas': datas,
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
