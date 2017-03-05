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
from openerp import models, fields, api


class Cards(models.Model):
    _name = 'credit_card'
    _description = 'Credit Cards'

    name = fields.Char('Tarjeta')
    surcharge = fields.Float('Recargo %')


class CardCommission(models.Model):
    _name = 'card_commission'
    _description = 'Card Commission'

    installment = fields.Integer('Cuotas')
    TNA = fields.Float('TNA')
    TEM = fields.Float('TEM')
    coefficient = fields.Float('Coeficiente', digits=(4, 4))
    card = fields.Many2one('credit_card')


class CreditPlan(models.Model):
    _name = 'credit_plan'
    _description = 'Credit Plan'
    _order = 'installments'

    name = fields.Char(compute="_compute_name")
    installments = fields.Integer('Cuotas')
    quota = fields.Float('Cuota', compute='_compute_quota')
    surcharge = fields.Float('Recargo')
    total = fields.Float('Total')

    @api.one
    @api.depends('installments', 'surcharge', 'total')
    def _compute_name(self):
        self.name = '{} cuotas de ${:.2f}       total ${:.2f}       (recargo ${:.2f})'.format(
                self.installments, self.quota, self.total, self.surcharge)

    @api.one
    @api.depends('installments', 'total')
    def _compute_quota(self):
        self.quota = self.total / self.installments
