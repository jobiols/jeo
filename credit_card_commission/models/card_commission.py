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
from openerp import models, fields


class Cards(models.Model):
    _name = 'credit_card'
    _description = 'Credit Cards'

    name = fields.Char('Tarjeta')


class CardCommission(models.Model):
    _name = 'card_commission'
    _description = 'Card Commission'

    installment = fields.Integer('Cuotas')
    TNA = fields.Float('TNA')
    TEM = fields.Float('TEM')
    coefficient = fields.Float('Coeficiente', digits=(4, 4))
    card = fields.Many2one('credit_card')
