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
from openerp import fields, models

from ...unit.backend_adapter import GenericAdapter
from ...backend import tienda_nube


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    tienda_nube_bind_ids = fields.One2many(
        comodel_name='tienda_nube.res.partner.category',
        inverse_name='odoo_id',
        string='TiendaNube Bindings',
        readonly=True,
    )


class TiendanubeResPartnerCategory(models.Model):
    _name = 'tienda_nube.res.partner.category'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'res.partner.category': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Partner Category',
        required=True,
        ondelete='cascade',
        oldname='openerp_id',
    )
    date_add = fields.Datetime(
        string='Created At (on TiendaNube)',
        readonly=True,
    )
    date_upd = fields.Datetime(
        string='Updated At (on TiendaNube)',
        readonly=True,
    )

    # TODO add tienda_nube shop when the field will be available in the api.
    # we have reported the bug for it
    # see http://forge.tienda_nube.com/browse/PSCFV-8284


@tienda_nube
class PartnerCategoryAdapter(GenericAdapter):
    _model_name = 'tienda_nube.res.partner.category'
    _tienda_nube_model = 'groups'
