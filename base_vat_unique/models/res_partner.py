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
#################################################################################

from openerp.osv import osv


class res_partner(osv.osv):
    def _check_unique_vat(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.document_type_id.name == 'CUIT':
                #            if partner.is_company:
                cr.execute("select vat from res_partner where upper(vat)=%s",
                           (partner.vat.upper(),))
                if len(cr.fetchall()) > 1:
                    return False
        return True

    _inherit = 'res.partner'
    _constraints = [
        (_check_unique_vat, u'El CUIT ya está ingresado', ['vat', 'is_company']),
    ]
