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
from openerp import models, fields, api
from openerp import SUPERUSER_ID
from openerp.exceptions import Warning


class product_product(models.Model):
    _inherit = 'product.template'

    prod_in_box = fields.Float(
            u'Cant producto por caja',
            help=u'Cantidad de metros cuadrados o lineales que entran en una caja'
    )
    prod_in_box_uom = fields.Selection([
        ('na', 'No aplica'),
        ('mt2', 'mts cuadrados'),
        ('mt', 'mts'),
    ],
            'Unidad', required=True,
            default='mt2'
    )
    price_1 = fields.Float(
            u'Publico',
            compute='_compute_prices'
    )
    price_2 = fields.Float(
            u'Obra',
            compute='_compute_prices'
    )
    price_3 = fields.Float(
            u'Efectivo',
            compute='_compute_prices'
    )

    @api.one
    @api.constrains('prod_in_box', 'prod_in_box_uom', 'type')
    def _check_prod_in_box(self):
        if self.prod_in_box_uom == 'na' and self.prod_in_box-0.0 > 0.001:
            raise Warning('Cantidad de producto por caja debe ser cero')

        if self.prod_in_box_uom != 'na' and self.type != 'product':
            raise Warning('Si aplica cantidad de producto por caja, '
                          'el tipo de producto debe ser almacenable')


    @api.one
    @api.depends('standard_price')
    def _compute_prices(self):
        _1_pricelist_id = 1  # Publico
        _2_pricelist_id = 4  # Obra
        _3_pricelist_id = 3  # Efectivo

        # calcular el precios basado en la lista de precios
        self.price_1 = self.pool.get('product.pricelist').price_get(
                self.env.cr, SUPERUSER_ID, [_1_pricelist_id], self.id, 1.0,
                context=None)[_1_pricelist_id]

        self.price_2 = self.pool.get('product.pricelist').price_get(
                self.env.cr, SUPERUSER_ID, [_2_pricelist_id], self.id, 1.0,
                context=None)[_2_pricelist_id]

        self.price_3 = self.pool.get('product.pricelist').price_get(
                self.env.cr, SUPERUSER_ID, [_3_pricelist_id], self.id, 1.0,
                context=None)[_3_pricelist_id]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
