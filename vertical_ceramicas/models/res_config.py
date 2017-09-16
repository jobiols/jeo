# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2017  jeo Software  (http://www.jeosoft.com.ar)
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


class PricelistConfiguration(models.TransientModel):
    _name = 'prices.config.settings'
    _inherit = 'res.config.settings'

    pricelist_1 = fields.Many2one(
            'product.pricelist',
            'Precio 1',
            default_model='prices.config.settings',
            help='Permite seleccionar la lista de precios para el precio 1'
    )
    pricelist_2 = fields.Many2one(
            'product.pricelist',
            'Precio 2',
            default_model='prices.config.settings',
            help='Permite seleccionar la lista de precios para el precio 2'
    )
    pricelist_3 = fields.Many2one(
            'product.pricelist',
            'Precio 3',
            default_model='prices.config.settings',
            help='Permite seleccionar la lista de precios para el precio 3'
    )

#    default_test = fields.Char('test', default_model='prices.config.settings')


    @api.model
    def get_default_pricelist_1(self, fields):
        confs = self.env['prices.config.settings'].search([], limit=1, order="id desc")
        return {'pricelist_1': confs.pricelist_1.id}

    @api.model
    def get_default_pricelist_2(self, fields):
        confs = self.env['prices.config.settings'].search([], limit=1, order="id desc")
        return {'pricelist_2': confs.pricelist_2.id}

    @api.model
    def get_default_pricelist_3(self, fields):
        confs = self.env['prices.config.settings'].search([], limit=1, order="id desc")
        return {'pricelist_3': confs.pricelist_3.id}
