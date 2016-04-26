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
from openerp import models, fields, api
from openerp.exceptions import except_orm


class sale_order(models.Model):
    _inherit = "sale.order"

    journal_id = fields.Many2one('account.journal', u'Método de pago', required='True')

    def _stock_move(self):
        # verificar que solo haya productos en la orden, sino no se puede transferir.
        lines = self.order_line.search([('order_id', '=', self.id)])
        for line in lines:
            if line.product_id.type != 'product':
                raise except_orm(
                    'Solo puede facturar productos con la facturación express!',
                    "El item '%s' en la orden de venta no es de tipo producto!" % (
                        line.name))

        # confirmar la orden de venta
        self.action_button_confirm()

        # mover el stock
        picking_obj = self.env['stock.picking']
        # encontrar los pickings que corresponden a la orden de venta

        for rec in picking_obj.search([('origin', '=', 'SO{:03.0f}'.format(self.id))]):

            # forzar para que funcione aunque no haya stock
            if not rec.force_assign():
                raise except_orm('No se pudo asignar el producto para la transferencia',
                                 'Error desconocido')

            # crear el Picking wizard
            self = self.with_context(active_model='stock.picking',
                                     active_ids=[rec.id])
            stock_transfer_picking_obj = self.env['stock.transfer_details']
            stock_transfer_picking = stock_transfer_picking_obj.create({})
            stock_transfer_picking.picking_id = rec.id
            stock_transfer_picking.do_detailed_transfer()

            self = self.with_context(active_id=rec.id)
            print_voucher_obj = self.env['stock.print_stock_voucher']
            voucher = print_voucher_obj.create({})
            voucher.book_id = 1

            voucher.get_estimated_number_of_pages()  # recalcular nro de paginas.

            pick = voucher.do_print_and_assign()

            # prepara la impresión del remito
            datas = {
                'ids': pick['context']['active_ids'],
                'model': 'stock.picking',
                'form': rec.read()
            }
            pick['datas'] = datas

            # imprrime el remito
            return pick

    @api.multi
    def button_express(self):
        return self._stock_move()

    @api.multi
    def button_invoice_express(self):
        self._stock_move()

        # crear la factura
        res = self.manual_invoice()

        # validar la factura
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.browse([res['res_id']])
        invoice.signal_workflow('invoice_open')


        res = invoice.invoice_pay_customer()
        context = res['context']

        journal = self.journal_id

        period_obj = self.env['account.period']
        period = period_obj.find()

        account_move_obj = self.env['account.move']
        account_move = account_move_obj.search([], limit=4)

        # pagar la factura
        # hacer configuracion para modificar esto
        receipt_obj = self.env['account.voucher.receiptbook']
        receipt = receipt_obj.search([('name', 'like', 'Recibos')], limit=1)

        account_voucher_obj = self.env['account.voucher']
        voucher = account_voucher_obj.create({
            'partner_id': context['default_partner_id'],
            'journal_id': journal.id,
            'account_id': journal.default_debit_account_id.id,
            'type': context['type'],
            'amount': context['default_amount'],
            'net_amount': context['default_amount'],
            'receiptbook_id': receipt.id,
            'company_id': self.env.user.id
        })
        voucher.signal_workflow('proforma_voucher')

        account_move_line_obj = self.env['account.move.line']

        # obtener un recordser vacio
        lines2rec = account_move_line_obj.browse()

        # obtener las lineas a conciliar de facturas
        account_move_line = account_move_line_obj.search(
            [('document_number', '=', invoice.document_number)])
        for re in account_move_line:
            if re.account_id.reconcile:
                lines2rec += re

        # obtener las lineas a conciliar de pagos
        account_move_line = account_move_line_obj.search(
            [('document_number', '=', voucher.document_number)])
        for re in account_move_line:
            if re.account_id.reconcile:
                lines2rec += re

        # reconciliar las lineas de factura con pagos
        lines2rec.reconcile('manual',
                            journal.default_debit_account_id.id,  # writeoff_acc_id
                            period.id,  # writeoff_period_id,
                            journal.id)  # writeoff_journal_id)

        datas = {
            'ids': invoice.ids,
            'model': 'account.report_invoice',
            'form': invoice.read()
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'aeroo_report_ar_einvoice',
            'datas': datas,
        }  # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
