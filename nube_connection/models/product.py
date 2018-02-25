# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import markdown
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class product_product(models.Model):
    _inherit = 'product.product'

    woo_categ = fields.Many2one(
        'curso.woo.categ',
        'Categoría Tienda Nube',
        help=u'Categoría Tienda Nube'
    )

    nube_id = fields.Integer(
        help=u'Identifica el producto en tienda nube'
    )

    description_short_wc = fields.Char(
        compute="_compute_short_wc",
        store="True"
    )

    published = fields.Boolean(
        'Publicado en tienda nube',
        help=u'Indica si se publica en tienda nube'
    )

    @api.one
    @api.depends('description')
    def _compute_short_wc(self):
        if self.description:
            ix = self.description.find('<mas>')
            if ix == -1:
                # no existe el simbolo <mas>
                if len(self.description) < 400:
                    self.description_short_wc = \
                        u'OK Total {} caracteres.'.format(len(self.description))
                else:
                    self.description_short_wc = \
                        u'Debe incluir el simbolo <mas> para reducir la cantidad de caracteres!!'
            else:
                # existe el simbolo <mas>
                if ix < 400:
                    self.description_short_wc = \
                        u'OK Total {} caracteres antes del símbolo <mas>'.format(ix)
                else:
                    self.description_short_wc = \
                        u'Total {} DEMASIADOS CARACTERES ANTES DE <mas> max 400'.format(ix)
