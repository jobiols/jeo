# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import models, fields
from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class SaleOrderState(models.Model):
    _name = 'sale.order.state'

    name = fields.Char('Name', translate=True)
    company_id = fields.Many2one(
            comodel_name='res.company',
            string='Company',
            required=True,
    )
    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.sale.order.state',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )


class TiendaNubeSaleOrderState(models.Model):
    _name = 'tienda_nube.sale.order.state'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'sale.order.state': 'odoo_id'}

    openerp_state_ids = fields.One2many(
            comodel_name='sale.order.state.list',
            inverse_name='tienda_nube_state_id',
            string='Odoo States',
    )
    odoo_id = fields.Many2one(
            comodel_name='sale.order.state',
            required=True,
            ondelete='cascade',
            string='Sale Order State',
            oldname='openerp_id',
    )


class SaleOrderStateList(models.Model):
    _name = 'sale.order.state.list'

    name = fields.Selection(
            selection=[
                ('draft', 'Draft Quotation'),
                ('sent', 'Quotation Sent'),
                ('cancel', 'Cancelled'),
                ('waiting_date', 'Waiting Schedule'),
                ('progress', 'Sales Order'),
                ('manual', 'Sale to Invoice'),
                ('invoice_except', 'Invoice Exception'),
                ('done', 'Done')
            ],
            string='Odoo State',
            required=True,
    )
    tienda_nube_state_id = fields.Many2one(
            comodel_name='tienda_nube.sale.order.state',
            string='TiendaNube State',
    )
    tienda_nube_id = fields.Integer(
            related='tienda_nube_state_id.tienda_nube_id',
            readonly=True,
            store=True,
            string='TiendaNube ID',
    )


@tienda_nube
class SaleOrderStateAdapter(GenericAdapter):
    _model_name = 'tienda_nube.sale.order.state'
    _tienda_nube_model = 'order_states'
