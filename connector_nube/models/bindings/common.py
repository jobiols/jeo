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
from openerp import api, fields, models

from openerp.addons.connector.session import ConnectorSession
from ...unit.importer import import_record


class TiendaNubeBinding(models.AbstractModel):
    _name = 'tienda_nube.binding'
    _inherit = 'external.binding'
    _description = 'TiendaNube Binding (abstract)'

    backend_id = fields.Many2one(
        comodel_name='tienda_nube.backend',
        string='TiendaNube Backend',
        required=True,
        ondelete='restrict'
    )
    tienda_nube_id = fields.Integer('ID on TiendaNube')

    _sql_constraints = [
        ('tienda_nube_uniq', 'unique(backend_id, tienda_nube_id)',
         'A record with same ID already exists on TiendaNube.'),
    ]

    @api.multi
    def resync(self):
        session = ConnectorSession(
            self.env.cr, self.env.uid, context=self.env.context)
        func = import_record
        if self.env.context and self.env.context.get('connector_delay'):
            func = import_record.delay
        for record in self:
            func(session, self._name, record.backend_id.id,
                 record.tienda_nube_id)
        return True


class TiendaNubeBindingOdoo(models.AbstractModel):
    _name = 'tienda_nube.binding.odoo'
    _inherit = 'tienda_nube.binding'
    _description = 'TiendaNube Binding with Odoo binding (abstract)'

    def _get_selection(self):
        records = self.env['ir.model'].search([])
        return [(r.model, r.name) for r in records] + [('', '')]

    # 'odoo_id': odoo-side id must be re-declared in concrete model
    # for having a many2one instead of a reference field
    odoo_id = fields.Reference(
        required=True,
        ondelete='cascade',
        string='Odoo binding',
        selection=_get_selection,
    )

    _sql_constraints = [
        ('tienda_nube_erp_uniq', 'unique(backend_id, odoo_id)',
         'An ERP record with same ID already exists on TiendaNube.'),
    ]
