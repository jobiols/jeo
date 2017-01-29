# -*- coding: utf-8 -*-
#####################################################################################
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
#####################################################################################
from openerp import models, fields

class product_category(models.Model):
    _inherit = 'product.category'

    discounts = fields.One2many('product.discount', 'categ_id')

    def search_child(self, name):
        return self.child_id.search([('name', '=', name), ('parent_id', '=', self.id)])

    def create_child(self, name):
        return self.child_id.create({'name': name, 'parent_id': self.id})

    def get_discount(self):
        if self.parent_id:
            ret = self.parent_id.get_discount()
        else:
            ret = 1.0
        for discount in self.discounts:
            ret *= (1 + discount.discount / 100)

        return ret

    def update_discounts(self, vals):
        for disc in self.discounts:
            disc.sudo().unlink()

        for val in vals:
            self.discounts.sudo().create(
                {'discount': val,
                 'categ_id': self.id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
