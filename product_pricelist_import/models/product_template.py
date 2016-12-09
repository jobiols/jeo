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
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class product_template(models.Model):
    _inherit = 'product.template'

    supplier_categ = fields.Char('Supplier', compute='_get_supplier_categ')
    standard_price_fake = fields.Float(digits_compute=dp.get_precision('Product Price'))
    standard_price = fields.Float(compute='_get_standard_price',
                                  digits_compute=dp.get_precision('Product Price'))

    @api.one
    def _get_standard_price(self):
        # si no hay proveedor el precio de lista del proveedor es cero.
        list_price = 0.0

        # obtener el precio de lista del proveedor
        for seller in self.seller_ids:
            list_price = seller.list_price

        # calcular el factor de descuento = (1 + descuento)
        # la categoria trae el producto de todas las categorias de la rama
        factor_discount = 1.0
        for categ in self.categ_id:
            factor_discount *= categ.sudo().get_discount()

        # calcular el precio de costo
        std_price = list_price * factor_discount

        # si cambió el precio, cambiarlo y almacenarlo en el histórico.
        if std_price <> self.standard_price_fake:
            self.standard_price_fake = std_price
            self.standard_price = std_price
            self.sudo()._set_standard_price(self._ids, std_price)

    @api.one
    def _get_supplier_categ(self):
        # si no hay proveedor avisar
        cat = 'Sin proveedor'
        # traer el nombre de la categoria del proveedor
        for supplierinfo in self.seller_ids:
            cat = supplierinfo.name.categ_id.name

        self.supplier_categ = cat



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
