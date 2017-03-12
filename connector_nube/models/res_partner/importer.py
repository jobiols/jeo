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
from datetime import datetime

from openerp.addons.connector.queue.job import job
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

from ...unit.importer import import_batch


@job(default_channel='root.tienda_nube')
def import_customers_since(session, backend_id, since_date=None):
    """ Prepare the import of partners modified on TiendaNube """

    print 'res_partner.importer.import_customer_since  --------->>> ', session, backend_id, since_date

    filters = None
    if since_date:
        filters = {
            'date': '1',
            'filter[date_upd]': '>[%s]' % (since_date)}
    now_fmt = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    import_batch(
            session, 'tienda_nube.res.partner.category', backend_id, filters
    )
    import_batch(
            session, 'tienda_nube.res.partner', backend_id, filters, priority=15
    )

    session.env['tienda_nube.backend'].browse(backend_id).write({
        'import_partners_since': now_fmt,
    })
