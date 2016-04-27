# -*- coding: utf-8 -*-
######################################################################################
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
######################################################################################
from openerp import models, api, fields


class product_template(models.Model):
    _inherit = 'product.product'

    @api.one
    def calculate_price(self):
        # obtener la ultima instancia del wizard
        wzrd = self.env['config.consult.product'].search([], limit=1, order='id desc')

        for rec in wzrd:
            data = rec.get_data()

            # calcular el precio basado en la lista de precios
            price = self.pool.get('product.pricelist').price_get(
                self.env.cr, self.env.uid, [data['pricelist']], self.id, 1.0,
                context=None)[data['pricelist']]

            if data['taxes']:
                for tax in self.taxes_id:
                    price = price * (1 + tax.amount)

            self.calculated_price = price
            self.calculated_pricelist = data['pricelist']

    @api.one
    def calculate_stock(self):
        self.stock = self.qty_available

    calculated_price = fields.Float(compute='calculate_price')
    calculated_pricelist = fields.Many2one('product.pricelist')
    stock = fields.Integer(compute='calculate_stock')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
