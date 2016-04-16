# -*- coding: utf-8 -*-
##################################################################################
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
##################################################################################
from openerp.osv import osv


class sale_order(osv.osv):
    _inherit = "sale.order"

    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines,
                              context=None):
        print 'on change pricelist --------------------------------------------'
        context = context or {}
        if not pricelist_id:
            print 'not pricelist id'
            return {}

        value = {
            'currency_id': self.pool.get('product.pricelist').browse(cr, uid,
                                                                     pricelist_id,
                                                                     context=context).currency_id.id
        }
        if not order_lines or order_lines == [(6, 0, [])]:
            print 'not order lines'
            return {'value': value}

        #########################
        print 'changed pricelist !!!!!!!!!!!!11'

        print 'pricelist id', pricelist_id
        print 'order lines', order_lines
        print context
        print '----------------------------------------------'

        sale_order_line_obj = self.pool['sale.order.line']
        sale_order_line = sale_order_line_obj.browse(cr, uid, order_lines[0][2])

        list_of_orderline = []
        for line in sale_order_line:
            line = {
                'order_id': line.order_id.id,
                'name': line.name,
                #                'product_id':line.product_id,
                #                'price_unit':line.price_unit,
                #                'tax_id':line.tax_id,
                #                'product_uom_qty':line.product_uom_qty,
            }
            list_of_orderline.append(line)
            print 'getting line ', line

        for line in sale_order_line:
            line.name = 9999
            print line.name


        #        print 'para borrar', order_lines[0][2]
        #        for id in order_lines[0][2]:
        #            sale_order_line_obj.unlink(cr, uid, id, context=context)

        print 'para crear'
        #        for values in list_of_orderline:
        #            print 'creando'
        #    sale_order_line_obj.create(cr,uid,values)

        #########################

        return {'value': value}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
