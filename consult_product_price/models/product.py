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
    _inherit = 'product.template'

    @api.one
    def calculate_price(self):
        print 'calculate prices ---------------------------------------',
        wzrd = self.env['config.consult.product'].search([])

        # obtener el ultimo ID
        rec = False
        for r in wzrd:
            rec = r

        if rec:
            print rec.pricelist_id.name

        self.calculated_price = 10.0

    calculated_price = fields.Float(compute='calculate_price')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
