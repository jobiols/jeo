# -*- coding: utf-8 -*-
# #######################################################################
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
# #######################################################################
from datetime import datetime

import pytz
from openerp import fields, models, api
from openerp.addons.connector.connector import ConnectorEnvironment
from openerp.addons.connector.session import ConnectorSession

from ..product_template.exporter import export_product_quantities
from ..res_partner.importer import import_customers_since
from ...unit.importer import import_batch


class TiendaNubeBackend(models.Model):
    _name = 'tienda_nube.backend'
    _description = 'Tienda Nube Backend'
    _inherit = 'connector.backend'

    _backend_type = 'tienda_nube'

    @api.model
    def _select_versions(self):
        """ Available versions

        Can be inherited to add custom versions.
        """
        return [('v1', 'Version 1')]

    version = fields.Selection(
            selection='_select_versions',
            string='Version',
            required=True,
    )
    location = fields.Char(string='Location')
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    default_lang_id = fields.Many2one(
            comodel_name='res.lang',
            string='Default Language',
    )
    import_partners_since = fields.Datetime('Import partners since')

    @api.multi
    def synchronize_metadata(self):
        print 'tienda_nube_backend.common.synchronize_metadata --------------------'
        session = ConnectorSession(
                self.env.cr, self.env.uid, context=self.env.context)
        for backend in self:
            for model in [
                'tienda_nube.shop.group',
                'tienda_nube.shop'
            ]:
                # import directly, do not delay because this
                # is a fast operation, a direct return is fine
                # and it is simpler to import them sequentially
                import_batch(session, model, backend.id)
        return True

    @api.multi
    def synchronize_basedata(self):
        session = ConnectorSession(
                self.env.cr, self.env.uid, context=self.env.context)
        for backend in self:
            for model_name in [
                'tienda_nube.res.lang',
                'tienda_nube.res.country',
                'tienda_nube.res.currency',
                'tienda_nube.account.tax',
            ]:
                env = get_environment(session, model_name, backend.id)
                directBinder = env.get_connector_unit(DirectBinder)
                directBinder.run()

            import_batch(session, 'tienda_nube.account.tax.group', backend.id)
            import_batch(session, 'tienda_nube.sale.order.state', backend.id)
        return True

    @api.multi
    def update_product_stock_qty(self):
        print 'tienda_nube_backend.update_product_stock_qty -------------------------------------'
        session = ConnectorSession(
                self.env.cr, self.env.uid, context=self.env.context)
        for backend_record in self:
            export_product_quantities.delay(session, backend_record.id)
        return True

    @api.multi
    def import_customers_since(self):
        print 'tienda_nube_backend.import_customers_since -------------------------------'
        session = ConnectorSession(
                self.env.cr, self.env.uid, context=self.env.context)
        for backend_record in self:
            since_date = self._date_as_user_tz(
                    backend_record.import_partners_since)
            import_customers_since.delay(
                    session,
                    backend_record.id,
                    since_date,
                    priority=10,
            )
        return True

    def _date_as_user_tz(self, dtstr):
        if not dtstr:
            return None
        timezone = pytz.timezone(self.env.user.partner_id.tz or 'utc')
        dt = datetime.strptime(dtstr, DEFAULT_SERVER_DATETIME_FORMAT)
        dt = pytz.utc.localize(dt)
        dt = dt.astimezone(timezone)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @api.multi
    def get_environment(self, model_name, session=None):
        print 'tienda_nube_backend.get_environment --------------------', model_name, '||', session
        self.ensure_one()
        if not session:
            print 'not session'
            session = ConnectorSession.from_env(self.env)

        return ConnectorEnvironment(self, session, model_name)
