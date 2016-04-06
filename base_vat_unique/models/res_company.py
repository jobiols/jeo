# -*- encoding: utf-8 -*-
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


class res_company(osv.osv):
    _inherit = 'res.company'

    def _get_partner_create(self, cr, uid, vals, context=None):
        res = super(res_company, self)._get_partner_create(cr, uid, vals, context=context)
        res['vat'] = vals.get('vat')
        return res
