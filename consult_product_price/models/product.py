# -*- coding: utf-8 -*-
######################################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
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

    def _calc_data(self):
        # obtener la ultima instancia del wizard
        wzrd = self.env['config.consult.product'].search([], limit=1, order='id desc')

        data = False
        for rec in wzrd:
            data = rec.get_data()

        return data

    @api.one
    def calculate_pricelist(self):
        # obtener la info de configuracion
        data = self._calc_data()
        if data:
            self.calculated_pricelist = data['pricelist_id']

    @api.one
    def calculate_price(self):
        # obtener la info de configuracion
        data = self._calc_data()
        if data:

            # calcular el precio basado en la lista de precios
            price = self.pool.get('product.pricelist').price_get(
                self.env.cr, self.env.uid, [data['pricelist_id']], self.id, 1.0,
                context=None)[data['pricelist_id']]

            if data['taxes']:
                for tax in self.taxes_id:
                    price = price * (1 + tax.amount)

            self.calculated_price = price


    @api.one
    def calculate_stock(self):
        self.stock = self.qty_available

    calculated_price = fields.Float(compute='calculate_price')
    calculated_pricelist = fields.Many2one('product.pricelist',
                                           compute='calculate_pricelist')
    stock = fields.Integer(compute='calculate_stock')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
