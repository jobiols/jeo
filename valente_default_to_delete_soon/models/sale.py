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

    # cuando cambia la lista de precios,
    # hace lo mismo que la original salvo que no muestra el cartel de que no se
    # actualizan los precios.
    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines,
                              context=None):
        context = context or {}
        if not pricelist_id:
            return {}

        value = {
            'currency_id': self.pool.get('product.pricelist'). \
                browse(cr, uid, pricelist_id, context=context).currency_id.id
        }
        if not order_lines or order_lines == [(6, 0, [])]:
            return {'value': value}

        return {'value': value}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
