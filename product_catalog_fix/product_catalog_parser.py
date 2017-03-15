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
from openerp.addons.product_catalog_aeroo_report.report.product_catalog_parser import Parser


class Parser(Parser):
    def get_products(self, category_ids, context=None):
        print 'get - products -------------------------------------------------------------------------'
        if not isinstance(category_ids, list):
            category_ids = [category_ids]

        if not context:
            context = {}
        order = context.get('products_order', '')
        only_with_stock = context.get('only_with_stock', False)
        category_type = context.get('category_type', False)
        if category_type == 'public_category':
            domain = [('public_categ_ids', 'in', category_ids)]
        else:
            domain = [('categ_id', 'in', category_ids)]
        if only_with_stock:
            domain.append(('qty_available', '>', 0))

        domain.append(('state', '!=', 'obsolete'))

        product_ids = self.pool[self.product_type].search(
                self.cr, self.uid, domain, order=order, context=context)

        products = self.pool[self.product_type].browse(
                self.cr, self.uid, product_ids, context=context)
        return products
