# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
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
# -----------------------------------------------------------------------------------
from openerp import fields, models, api


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # lo ponemos readonly para todos y despues lo dejamos editar con permisos
    price_unit = fields.Float(states={'draft': [('readonly', True)]})

    @api.model
    def product_id_change(self, ppp, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False, lang=False,
            update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False):
        """ Hereda de la funcion product_id_change que es llamada cuando cambia el producto
            o la cantidad, se intercepta el res y se le agrega m2 en el name
        """

        res = super(sale_order_line, self).product_id_change(
            pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang,
            update_tax, date_order, packaging, fiscal_position, flag)

        if product:
            prod = self.env['product.product'].search([('id', '=', product)])
            if prod.prod_in_box <> 0:
                # agregamos los metros cuadrados, al value/name. A veces el super decide
                # que no tiene que modificar el name entonces no está en el dict, en ese caso
                # lo agrego y le pongo el name_get + los metros cuadrados
                try:
                    res['value']['name'] += u' Total {} {}'.format(
                        prod.prod_in_box * qty,
                        prod.prod_in_box_uom)
                except:
                    res['value']['name'] = u'{} Total {} {}'.format(
                        prod.name_get()[0][1],
                        prod.prod_in_box * qty,
                        prod.prod_in_box_uom)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
