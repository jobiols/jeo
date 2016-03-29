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

    def get_discount(self):
        print '>> get_discount cat', self.name
        if self.parent_id:
            ret = self.parent_id.get_discount()
        else:
            ret = 1.0
        print 'ret', ret
        for discount in self.discounts:
            ret *= (1 + discount.discount / 100)
            print 'discount', discount.discount

        print '<< get_discount cat', self.name, 'ret=', ret
        return ret

    def update_discounts(self, vals):
        print 'update discounts ----------------', vals
        for disc in self.discounts:
            print 'unlinking '
            disc.unlink()

        for val in vals:
            print 'creating ', val
            self.discounts.create(
                {'discount': val,
                 'categ_id': self.id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
