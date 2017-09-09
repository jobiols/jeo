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


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # es el comentario del deposito se usa en el remito para decir donde se retira y a que hora etc.
    pick_from = fields.Char(
            string="retira",
            compute="_get_picking_location"
    )

    @api.one
    def _get_picking_location(self):
        for line in self.move_lines:
            loc = line.location_id
            self.pick_from = loc.comment


class StockMove(models.Model):
    _inherit = "stock.move"

    # es la direccion de entrega
    partner_shipping_id = fields.Many2one(
            'res.partner',
            'Direccion de entrega',
            compute='_get_partner_shipping_id'
    )

    @api.one
    @api.depends('partner_id.child_ids')
    def _get_partner_shipping_id(self):
        addresses = self.partner_id.child_ids.search([('type', '=', 'delivery')])
        # me traigo solo la primera si es que existe
        for address in addresses:
            self.partner_shipping_id = address.id



