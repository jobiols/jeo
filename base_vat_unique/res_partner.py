# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2013 Cubic ERP - Teradata SAC. (http://cubicerp.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _


class res_partner(osv.osv):
    def _check_unique_vat(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.is_company:
                cr.execute("select vat from res_partner where upper(vat)=%s",
                           (partner.vat.upper(),))
                if len(cr.fetchall()) > 1:
                    return False
        return True

    _inherit = 'res.partner'
    _constraints = [
        (_check_unique_vat,
         'The VAT Number must be unique, use CC prefix for custom codes differtent from VAT',
         ['vat', 'is_company']),
    ]
