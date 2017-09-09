# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------
from openerp import models, fields, api


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    # lo ponemos readonly para todos y despues lo dejamos editar con permisos
    price_unit = fields.Float(readonly=True)

    @api.one
    def _compute_price(self):
        """ Hereda de la funcion _compute_price que es llamada con un @depends cuando
            cambia la cantidad entre otras cosas el name agregando el total de metros o
            metros cuadrados de producto que hay en al caja.
        """
        super(account_invoice_line,self)._compute_price()
        if self.product_id.prod_in_box <> 0:
            self.name = u'{} Total {} {}'.format(self.product_id.name,
                                             self.product_id.prod_in_box*self.quantity,
                                             self.product_id.prod_in_box_uom)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
