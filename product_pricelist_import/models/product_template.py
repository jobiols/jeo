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
import openerp.addons.decimal_precision as dp


class product_template(models.Model):
    _inherit = 'product.template'

    supplier_categ = fields.Char(compute='_get_supplier_categ', string="Supplier")
    standard_price_fake = fields.Float(digits_compute=dp.get_precision('Product Price'))
    standard_price = fields.Float(compute='_get_standard_price',
                                  digits_compute=dp.get_precision('Product Price'))

    def _get_standard_price(self):
        list_price = 0.0
        for seller in self.seller_ids:
            list_price = seller.list_price
            break

        factor_discount = 1.0
        for categ in self.categ_id:
            factor_discount *= categ.get_discount()

        std_price = list_price * factor_discount

        if std_price <> self.standard_price_fake:
            self.standard_price_fake = std_price
            self.standard_price = std_price
            self._set_standard_price(self._ids, std_price)

    def _get_supplier_categ(self):
        print '--------------------------------------------'
        ret = 'categoria del proveedor'
        print ret
        return ret



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
