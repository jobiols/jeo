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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class account_invoice(models.Model):
    _inherit = "account.invoice"

    cc_tax_10 = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string='IVA 10.5%',
    )

    cc_tax_21 = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string='IVA 21%',
    )

    cc_tax_27 = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string='IVA 27%',
    )

    cc_tax_exempt = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string='No Gravado',
    )

    cc_perc_IIBB = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string=u'Percepción IIBB',
    )

    cc_perc_iva = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string=u'Percepción IVA',
    )

    cc_base = fields.Float(
        compute="_get_values",
        digits=dp.get_precision('Account'),
        string=u'Base imponible',
    )

    @api.one
    def _get_values(self):

        if False:
            print '------------------------------------------------------ ', doc_code
            print 'printed_amount_untaxed={} ' \
                  'printed_amount_tax={} ' \
                  'vat_amount={} ' \
                  'other_taxes_amount={} ' \
                  'vat_exempt_amount={} ' \
                  'vat_untaxed={} ' \
                  'vat_base_amount={}'.format(
                self.printed_amount_untaxed,
                self.printed_amount_tax,
                self.vat_amount,
                self.other_taxes_amount,
                self.vat_exempt_amount,
                self.vat_untaxed,
                self.vat_base_amount)
            print 'printed_tax_ids --'
            for tax in self.printed_tax_ids:
                print tax.base, tax.amount, tax.name

            print 'vat_tax_ids --'
            for tax in self.vat_tax_ids:
                print tax.base, tax.amount, tax.name

            print 'not_vat_tax_ids --'
            for tax in self.not_vat_tax_ids:
                print tax.base, tax.amount, tax.name

        # calcular el iva para las tres columnas 10.5 21 y 27
        # y la base imponible gravada
        for tax in self.vat_tax_ids:
            if ('IVA Compras 10.5%' in tax.name or 'IVA Ventas 10.5%' in tax.name):
                self.cc_tax_10 += tax.amount

            if ('IVA Compras 21%' in tax.name or 'IVA Ventas 21%' in tax.name):
                self.cc_tax_21 += tax.amount

            if ('IVA Compras 27%' in tax.name or 'IVA Compras 27%' in tax.name):
                self.cc_tax_27 += tax.amount

            # Calcular la base imponible sumanto las bases de todos los iva gravados
            if 'IVA' in tax.name:
                if tax.amount != 0:
                    self.cc_base += tax.base

        # calcular percepciones IIBB e Iva
        for tax in self.not_vat_tax_ids:
            if 'Perc IIBB' in tax.name:
                self.cc_perc_IIBB += tax.amount

            if 'Perc IVA' in tax.name:
                self.cc_perc_iva += tax.amount

        # calcular exento por diferencia
        tax_exempt = self.cc_amount_total - \
                     self.cc_base - \
                     self.cc_perc_iva - \
                     self.cc_perc_IIBB - \
                     self.cc_tax_27 - \
                     self.cc_tax_21 - \
                     self.cc_tax_10

        # filtrar el error de redondeo
        if (abs(tax_exempt) > 0.05):
            self.cc_tax_exempt = tax_exempt

    @api.multi
    def check_argentinian_invoice_taxes(self):
        """
        We make theis function to be used as a constraint but also to be called
        from other models like vat citi
        """
        # only check for argentinian localization companies
        _logger.info('Running checks related to argentinian documents')

        # we consider argentinian invoices the ones from companies with
        # use_argentinian_localization and that belongs to a journal with
        # use_documents
        argentinian_invoices = self.filtered(
            lambda r: (
                r.use_argentinian_localization and r.use_documents))
        if not argentinian_invoices:
            return True

        # check invoice tax has code
        without_tax_code = self.env['account.invoice.tax'].search([
            ('invoice_id', 'in', argentinian_invoices.ids),
            ('tax_code_id', '=', False),
        ])
        if without_tax_code:
            raise Warning(_(
                "You are using argentinian localization and there are some "
                "invoices with taxes that don't have tax code, tax code is "
                "required to generate this report. Invoies ids: %s" % (
                    without_tax_code.mapped('invoice_id.id'))))

        # check codes has argentinian tax attributes configured
        tax_codes = argentinian_invoices.mapped('tax_line.tax_code_id')
        unconfigured_tax_codes = tax_codes.filtered(
            lambda r: not r.type or not r.tax or not r.application)
        if unconfigured_tax_codes:
            raise Warning(_(
                "You are using argentinian localization and there are some tax"
                " codes that are not configured. Tax codes ids: %s" % (
                    unconfigured_tax_codes.ids)))

        # eliminamos el chequeo de invoice without amount
        # Check invoice with amount
        #       invoices_without_amount = self.search([
        #           ('id', 'in', argentinian_invoices.ids),
        #           ('amount_total', '=', 0.0)])
        #       if invoices_without_amount:
        #           raise Warning(_('Invoices ids %s amount is cero!') % (
        #               invoices_without_amount.ids))

        # Check invoice requiring vat

        # out invoice must have vat if are argentinian and from a company with
        # responsability that requires vat
        sale_invoices_with_vat = self.search([(
            'id', 'in', argentinian_invoices.ids),
            ('type', 'in', ['out_invoice', 'out_refund']),
            ('company_id.partner_id.responsability_id.vat_tax_required_on_sales_invoices',
             '=', True)])

        # check purchase invoice has supplier invoice number
        purchase_invoices = argentinian_invoices.filtered(
            lambda r: r.type in ('in_invoice', 'in_refund'))
        purchase_invoices_without_sup_number = purchase_invoices.filtered(
            lambda r: (not r.supplier_invoice_number))
        if purchase_invoices_without_sup_number:
            raise Warning(_(
                "Some purchase invoices don't have supplier nunmber.\n"
                "Invoices ids: %s" % purchase_invoices_without_sup_number.ids))

        # purchase invoice must have vat if document class letter has vat
        # discriminated
        purchase_invoices_with_vat = purchase_invoices.filtered(
            lambda r: (
                r.afip_document_class_id.document_letter_id.vat_discriminated))

        invoices_with_vat = (
            sale_invoices_with_vat + purchase_invoices_with_vat)

        for invoice in invoices_with_vat:
            # we check vat base amount is equal to amount untaxed
            # usamos una precision de 0.1 porque en algunos casos no pudimos
            # arreglar pbñe,as de redondedo
            if abs(invoice.vat_base_amount - invoice.amount_untaxed) > 0.1:
                raise Warning(_(
                    "Invoice ID: %i\n"
                    "Invoice subtotal (%.2f) is different from invoice base"
                    " vat amount (%.2f)" % (
                        invoice.id,
                        invoice.amount_untaxed,
                        invoice.vat_base_amount)))

        # check purchase invoices that can't have vat. We check only the ones
        # with document letter because other documents may have or not vat tax
        purchase_invoices_without = purchase_invoices.filtered(
            lambda r: (
                r.afip_document_class_id.document_letter_id and
                not r.afip_document_class_id.document_letter_id.vat_discriminated))
        for invoice in purchase_invoices_without:
            if invoice.vat_tax_ids:
                raise Warning(_(
                    "Invoice ID %i shouldn't have any vat tax" % invoice.id))




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
