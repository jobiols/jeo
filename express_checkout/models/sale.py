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
from openerp.exceptions import except_orm, Warning, RedirectWarning

class sale_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def button_invoice_express(self):
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> button invoice express'
        # verificar que solo haya productos en la orden, sino no se puede transferir.
        lines = self.order_line.search([('order_id', '=', self.id)])
        for line in lines:
            if line.product_id.type != 'product':
                raise except_orm(
                    'Solo puede facturar productos con la facturación express!',
                    "El item '%s' en la orden de venta no es de tipo producto!" % (
                    line.name))

        print '------------------------------------------------- confirmar orden de venta'
        # confirmar la orden de venta
        print '>', self.action_button_confirm()

        print '--------------------------------------------------------- mover materiales'
        # mover el stock
        picking_obj = self.env['stock.picking']
        # encontrar los pickings que corresponden a la orden de venta
        for rec in picking_obj.search([('origin', '=', 'SO{:03.0f}'.format(self.id))]):
            # forzar para que funcione aunque no haya stock
            if not rec.force_assign():
                raise except_orm('No se pudo asignar el producto para la transferencia',
                                 'Error desconocido')
            # hacer finalmente la transferencia
            if not rec.do_transfer():
                raise except_orm('No se pudo transferir el material',
                                 'Error desconocido')

        print '------------------------------------------------------------ crear factura'
        # crear la factura
        res = self.manual_invoice()
        print '>', res

        print '---------------------------------------------------------- validar factura'
        # validar la factura
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.browse([res['res_id']])
        invoice.signal_workflow('invoice_open')

        print '------------------------------------------------------------ pagar factura'
        # pagar la factura
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
            'report_name': 'aeroo_report_ar_einvoice',
            'datas': datas,
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
