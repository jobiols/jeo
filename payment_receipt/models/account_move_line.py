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
from openerp import models, api, fields, _


class account_move_line(models.Model):
    _inherit = "account.move.line"

    to_pay = fields.Float(
        compute='_compute_to_pay'
    )

    @api.depends('payment_ids')
    @api.one
    def _compute_to_pay(self):
        ret = 0
        for line in self.payment_ids:
            ret -= line.credit

        for line in self.invoice_line:
            ret += line.amount_total

        self.to_pay = ret
