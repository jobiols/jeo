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

class account_invoice(models.Model):
    _inherit = "account.invoice"

    state_id = fields.Many2one(
        related='commercial_partner_id.state_id',
        store=True,
    )
    currency_rate = fields.Float(
        string='Currency Rate',
        compute='_get_currency_values',
        help='Currency Rate for this currency on invoice date or today '
             '(if not date)',
        digits=(12, 6)
        # Usamos muchos decimales por el citi (requiere) y para buen calculo
        # TODO hacer editable en draft con funcion inverse que cree cotizacion
        # set='_get_currency_rate',
        # readonly=True,
        # states={'draft': [('readonly', False)]}
    )
    invoice_number = fields.Integer(
        compute='_get_invoice_number',
        string=_("Invoice Number"),
    )
    point_of_sale = fields.Integer(
        compute='_get_invoice_number',
        string=_("Point Of Sale"),
    )
    printed_amount_tax = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string=_('Tax')
    )
    printed_amount_untaxed = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string=_('Subtotal')
    )
    # no gravado en iva
    vat_untaxed = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string=_('VAT Untaxed')
    )
    # no gravado en iva
    cc_vat_untaxed = fields.Float(
        compute="_get_currency_values",
        digits=dp.get_precision('Account'),
        string='Company Cur. VAT Untaxed',
    )
    # company currency default odoo fields
    cc_amount_total = fields.Float(
        compute="_get_currency_values",
        digits=dp.get_precision('Account'),
        string='Company Cur. Total',
    )
    cc_amount_untaxed = fields.Float(
        compute="_get_currency_values",
        digits=dp.get_precision('Account'),
        string='Company Cur. Untaxed',
    )
    cc_amount_tax = fields.Float(
        compute="_get_currency_values",
        digits=dp.get_precision('Account'),
        string='Company Cur. Tax',
    )
    # exento en iva
    vat_exempt_amount = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string=_('VAT Exempt Amount')
    )
    # von iva
    vat_amount = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string='VAT Amount',
    )
    # von iva
    cc_vat_amount = fields.Float(
        compute="_get_currency_values",
        digits=dp.get_precision('Account'),
        string='Company Cur. VAT Amount',
    )
    # von iva
    vat_base_amount = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string=_('VAT Base Amount')
    )
    other_taxes_amount = fields.Float(
        compute="_get_taxes_and_prices",
        digits=dp.get_precision('Account'),
        string='Other Taxes Amount',
    )
    cc_other_taxes_amount = fields.Float(
        compute="_get_currency_values",
        digits=dp.get_precision('Account'),
        string='Company Cur. Other Taxes Amount'
    )
    printed_tax_ids = fields.One2many(
        compute="_get_taxes_and_prices",
        comodel_name='account.invoice.tax',
        string=_('Tax')
    )
    vat_tax_ids = fields.One2many(
        compute="_get_taxes_and_prices",
        comodel_name='account.invoice.tax',
        string=_('VAT Taxes')
    )
    not_vat_tax_ids = fields.One2many(
        compute="_get_taxes_and_prices",
        comodel_name='account.invoice.tax',
        string=_('Not VAT Taxes')
    )
    vat_discriminated = fields.Boolean(
        _('Discriminate VAT?'),
        compute="get_vat_discriminated",
        help=_("Discriminate VAT on Invoices?"),
    )
    available_journal_document_class_ids = fields.Many2many(
        'account.journal.afip_document_class',
        compute='_get_available_journal_document_class',
        string=_('Available Journal Document Classes'),
    )
    supplier_invoice_number = fields.Char(
        copy=False,
    )
    journal_document_class_id = fields.Many2one(
        'account.journal.afip_document_class',
        'Document Type',
        readonly=True,
        ondelete='restrict',
        states={'draft': [('readonly', False)]}
    )
    afip_incoterm_id = fields.Many2one(
        'afip.incoterm',
        'Incoterm',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    afip_document_class_id = fields.Many2one(
        'afip.document_class',
        related='journal_document_class_id.afip_document_class_id',
        string='Document Type',
        copy=False,
        readonly=True,
        store=True,
    )
    afip_document_number = fields.Char(
        string='Document Number',
        copy=False,
        readonly=True,
    )
    responsability_id = fields.Many2one(
        'afip.responsability',
        string='Responsability',
        readonly=True,
        copy=False,
    )
    formated_vat = fields.Char(
        string='Responsability',
        related='commercial_partner_id.formated_vat',
    )
    document_number = fields.Char(
        compute='_get_document_number',
        # string=_('Document Number'),
        # waiting for a PR 9081 to fix computed fields translations
        string='Número de documento',
        readonly=True,
    )
    next_invoice_number = fields.Integer(
        compute='_get_next_invoice_number',
        string='Next Document Number',
        readonly=True
    )
    use_documents = fields.Boolean(
        related='journal_id.use_documents',
        string='Use Documents?',
        readonly=True
    )
    use_argentinian_localization = fields.Boolean(
        related='company_id.use_argentinian_localization',
        string='Use Argentinian Localization?',
        readonly=True,
    )
    point_of_sale_type = fields.Selection(
        related='journal_id.point_of_sale_id.type',
        readonly=True,
    )
    # estos campos los agregamos en este modulo pero en realidad los usa FE
    # pero entendemos que podrian ser necesarios para otros tipos, por ahora
    # solo lo vamos a hacer requerido si el punto de venta es del tipo
    # electronico
    afip_concept = fields.Selection(
        compute='_get_concept',
        # store=True,
        selection=[('1', 'Producto / Exportación definitiva de bienes'),
                   ('2', 'Servicios'),
                   ('3', 'Productos y Servicios'),
                   ('4', '4-Otros (exportación)'),
                   ],
        string="AFIP concept",
    )
    afip_service_start = fields.Date(
        string='Service Start Date'
    )
    afip_service_end = fields.Date(
        string='Service End Date'
    )
