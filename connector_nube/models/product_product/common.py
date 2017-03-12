# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp

from ...backend import tienda_nube
from ...unit.backend_adapter import GenericAdapter


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.combination',
            inverse_name='odoo_id',
            copy=False,
            string='TiendaNube Bindings',
    )
    tienda_nube_combinations_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.combination',
            inverse_name='odoo_id',
            string='TiendaNube Bindings (combinations)',
    )
    default_on = fields.Boolean(string='Default On')
    impact_price = fields.Float(
            string="Price Impact", digits=dp.get_precision('Product Price'))

    @api.multi
    @api.depends('impact_price', 'product_tmpl_id.list_price')
    def _compute_lst_price(self):
        for product in self:
            price = product.list_price + product.impact_price
            if 'uom' in self.env.context:
                uom = product.uos_id or product.uom_id
                price = uom._compute_price(
                        product.uom_id.id, price, self.env.context['uom'])
            product.lst_price = price

    lst_price = fields.Float(
            compute='_compute_lst_price')

    @api.multi
    def _set_variants_default_on(self, default_on_list=None):
        if self.env.context.get('skip_check_default_variant', False):
            return True
        templates = self.mapped('product_tmpl_id')
        for template in templates:
            variants = template.with_context(
                    skip_check_default_variant=True
            ).product_variant_ids.filtered('default_on')
            if not variants:
                active_variants = template.with_context(
                        skip_check_default_variant=True
                ).product_variant_ids.filtered('active')
                active_variants[:1].write({'default_on': True})
            elif len(variants) > 1:
                if default_on_list:
                    variants.filtered(
                            lambda x: x.id not in default_on_list
                    ).write({'default_on': False})
                else:
                    variants[1:].write({'default_on': False})

    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        res._set_variants_default_on()
        return res

    @api.multi
    def write(self, vals):
        if not vals.get('active', True):
            vals['default_on'] = False
        res = super(ProductProduct, self).write(vals)
        default_on_list = vals.get('default_on', False) and self.ids or []
        self._set_variants_default_on(default_on_list)
        return res

    @api.multi
    def unlink(self):
        self.write({
            'default_on': False,
            'active': False
        })
        res = super(ProductProduct, self).unlink()
        return res

    @api.multi
    def update_tienda_nube_qty(self):
        for product in self:
            if product.product_variant_count > 1:
                # Recompute qty in combination binding
                for combination_binding in product.tienda_nube_bind_ids:
                    combination_binding.recompute_tienda_nube_qty()
            # Recompute qty in product template binding if any combination
            # if modified
            for tienda_nube_product in \
                    product.product_tmpl_id.tienda_nube_bind_ids:
                tienda_nube_product.recompute_tienda_nube_qty()

    @api.multi
    def update_tienda_nube_quantities(self):
        for product in self:
            product_template = product.product_tmpl_id
            tienda_nube_combinations = (
                                           len(product_template.product_variant_ids) > 1 and
                                           product_template.product_variant_ids) or []
            if not tienda_nube_combinations:
                for tienda_nube_product in product_template.tienda_nube_bind_ids:
                    tienda_nube_product.recompute_tienda_nube_qty()
            else:
                for tienda_nube_combination in tienda_nube_combinations:
                    for combination_binding in \
                            tienda_nube_combination.tienda_nube_bind_ids:
                        combination_binding.recompute_tienda_nube_qty()
        return True

    @api.multi
    def open_product_template(self):
        """
        Utility method used to add an "Open Product Template"
        button in product.product views
        """
        self.ensure_one()
        return {'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': self.product_tmpl_id.id,
                'target': 'new',
                'flags': {'form': {'action_buttons': True}}}


class TiendaNubeProductCombination(models.Model):
    _name = 'tienda_nube.product.combination'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'product.product': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.product',
            string='Product',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    main_template_id = fields.Many2one(
            comodel_name='tienda_nube.product.template',
            string='Main Template',
            required=True,
            ondelete='cascade',
    )
    quantity = fields.Float(
            string='Computed Quantity',
            help='Last computed quantity to send on TiendaNube.'
    )
    reference = fields.Char(string='Original reference')

    @api.multi
    def recompute_tienda_nube_qty(self):
        for product_binding in self:
            if product_binding.quantity != product_binding.qty_available:
                product_binding.quantity = product_binding.qty_available
        return True

    @api.model
    def _tienda_nube_qty(self, product):
        return product.qty_available


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.combination.option',
            inverse_name='odoo_id',
            string='TiendaNube Bindings (combinations)',
    )


class TiendaNubeProductCombinationOption(models.Model):
    _name = 'tienda_nube.product.combination.option'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'product.attribute': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.attribute',
            string='Attribute',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    tienda_nube_position = fields.Integer('TiendaNube Position')
    group_type = fields.Selection([
        ('color', 'Color'),
        ('radio', 'Radio'),
        ('select', 'Select')], string='Type', default='select')
    public_name = fields.Char(string='Public Name', translate=True)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.combination.option.value',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )


class TiendaNubeProductCombinationOptionValue(models.Model):
    _name = 'tienda_nube.product.combination.option.value'
    _inherit = 'tienda_nube.binding'
    _inherits = {'product.attribute.value': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='product.attribute.value',
            string='Attribute',
            required=True,
            ondelete='cascade',
            oldname='openerp_id',
    )
    tienda_nube_position = fields.Integer(
            string='TiendaNube Position',
            default=1,
    )
    id_attribute_group = fields.Many2one(
            comodel_name='tienda_nube.product.combination.option')


@tienda_nube
class ProductCombinationAdapter(GenericAdapter):
    _model_name = 'tienda_nube.product.combination'
    _tienda_nube_model = 'combinations'
    _export_node_name = 'combination'


@tienda_nube
class ProductCombinationOptionAdapter(GenericAdapter):
    _model_name = 'tienda_nube.product.combination.option'
    _tienda_nube_model = 'product_options'
    _export_node_name = 'product_options'
