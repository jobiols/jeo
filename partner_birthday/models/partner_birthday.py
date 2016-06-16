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
from datetime import datetime, date

from openerp import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.one
    def _get_birthday(self):
        if self.date:
            dt = datetime.strptime(self.date, '%Y-%m-%d')
            month = datetime.strftime(dt, '%m')
            day = datetime.strftime(dt, '%d')
            self.birthday = datetime(year=date.today().year,
                                     month=int(month),
                                     day=int(day)).strftime('%d/%m/%Y')

    birthday = fields.Char(compute='_get_birthday', string=u'Cumpleaños')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
