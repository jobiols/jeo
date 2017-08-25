# -*- coding: utf-8 -*-
####################################################################################
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
####################################################################################
from openerp import models, fields, api

# Crea wizard para configurar consulta de precios

class config_consult_product(models.Model):
    _name = "config.consult.product"
    _description = "Configuracion de la consulta de precios"

    pricelist_id = fields.Many2one(
        'product.pricelist', domain=[('type', '=', 'sale'), ], default=3)

    taxes = fields.Boolean(
        'Con impuestos', default=True)

    @api.one
    def button_save_config(self):
        return True

    def get_data(self):
        return {
            'pricelist_id': self.pricelist_id.id,
            'taxes': self.taxes
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
