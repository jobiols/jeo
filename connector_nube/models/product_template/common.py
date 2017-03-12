# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from openerp import api, fields, models

try:
    from xml.etree import cElementTree as ElementTree
except ImportError, e:
    from xml.etree import ElementTree

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube

_logger = logging.getLogger(__name__)

try:
    from prestapyt import TiendaNubeWebServiceDict, TiendaNubeWebServiceError
except ImportError:
    _logger.debug('Can not `from prestapyt import TiendaNubeWebServiceDict '
                  'or TiendaNubeWebServiceError`.')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.template',
            inverse_name='odoo_id',
            copy=False,
            string='TiendaNube Bindings',
    )

    @api.multi
    def update_tienda_nube_quantities(self):
        for template in self:
            # Recompute product template TiendaNube qty
            template.mapped('tienda_nube_bind_ids').recompute_tienda_nube_qty()
            # Recompute variant TiendaNube qty
            template.mapped(
                    'product_variant_ids.tienda_nube_bind_ids'
            ).recompute_tienda_nube_qty()
        return True


class TiendaNubeProductTemplate(models.Model):
    _name = 'tienda_nube.product.template'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'product.template': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.template',
            required=True,
            ondelete='cascade',
            string='Template',
            oldname='openerp_id',
    )
    # TODO FIXME what name give to field present in
    # tienda_nube_product_product and product_product
    always_available = fields.Boolean(
            string='Active',
            default=True,
            help='If checked, this product is considered always available')
    quantity = fields.Float(
            string='Computed Quantity',
            help="Last computed quantity to send to TiendaNube."
    )
    description_html = fields.Html(
            string='Description',
            translate=True,
            help="HTML description from TiendaNube",
    )
    description_short_html = fields.Html(
            string='Short Description',
            translate=True,
    )
    date_add = fields.Datetime(
            string='Created at (in TiendaNube)',
            readonly=True
    )
    date_upd = fields.Datetime(
            string='Updated at (in TiendaNube)',
            readonly=True
    )
    default_shop_id = fields.Many2one(
            comodel_name='tienda_nube.shop',
            string='Default shop',
            required=True
    )
    link_rewrite = fields.Char(
            string='Friendly URL',
            translate=True,
    )
    available_for_order = fields.Boolean(
            string='Available for Order Taking',
            default=True,
    )
    show_price = fields.Boolean(string='Display Price', default=True)
    combinations_ids = fields.One2many(
            comodel_name='tienda_nube.product.combination',
            inverse_name='main_template_id',
            string='Combinations'
    )
    reference = fields.Char(string='Original reference')
    on_sale = fields.Boolean(string='Show on sale icon')

    @api.multi
    def recompute_tienda_nube_qty(self):
        for product_binding in self:
            new_qty = product_binding._tienda_nube_qty()
            if product_binding.quantity != new_qty:
                product_binding.quantity = new_qty
        return True

    def _tienda_nube_qty(self):
        locations = self.env['stock.location'].search([
            ('id', 'child_of', self.backend_id.warehouse_id.lot_stock_id.id),
            ('tienda_nube_synchronized', '=', True),
            ('usage', '=', 'internal'),
        ])
        return self.with_context(location=locations.ids).qty_available


@tienda_nube
class TemplateAdapter(GenericAdapter):
    _model_name = 'tienda_nube.product.template'
    _tienda_nube_model = 'products'
    _export_node_name = 'product'


@tienda_nube
class ProductInventoryAdapter(GenericAdapter):
    _model_name = '_import_stock_available'
    _tienda_nube_model = 'stock_availables'
    _export_node_name = 'stock_available'

    def get(self, options=None):
        return self.client.get(self._tienda_nube_model, options=options)

    def export_quantity(self, filters, quantity):
        self.export_quantity_url(
                filters,
                quantity,
        )

        shops = self.env['tienda_nube.shop'].search([
            ('backend_id', '=', self.backend_record.id),
            ('default_url', '!=', False),
        ])
        for shop in shops:
            url = '%s/api' % shop.default_url
            key = self.backend_record.webservice_key
            client = TiendaNubeWebServiceDict(url, key)
            self.export_quantity_url(filters, quantity, client=client)

    def export_quantity_url(self, filters, quantity, client=None):
        if client is None:
            client = self.client
        response = client.search(self._tienda_nube_model, filters)
        for stock_id in response:
            res = client.get(self._tienda_nube_model, stock_id)
            first_key = res.keys()[0]
            stock = res[first_key]
            stock['quantity'] = int(quantity)
            try:
                client.edit(
                        self._tienda_nube_model, {self._export_node_name: stock})
            # TODO: investigate the silent errors
            except TiendaNubeWebServiceError:
                pass
            except ElementTree.ParseError:
                pass


@tienda_nube
class TiendaNubeProductTags(GenericAdapter):
    _model_name = '_tienda_nube_product_tag'
    _tienda_nube_model = 'tags'
    _export_node_name = 'tag'

    def search(self, filters=None):
        res = self.client.get(self._tienda_nube_model, options=filters)
        tags = res[self._tienda_nube_model][self._export_node_name]
        if isinstance(tags, dict):
            return [tags]
        return tags
