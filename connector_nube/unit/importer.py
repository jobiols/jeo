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
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.synchronizer import Importer


class BatchImporter(Importer):
    """ The role of a BatchImporter is to search for a list of
    items to import, then it can either import them directly or delay
    the import of each item separately.
    """
    page_size = 1000

    def run(self, filters=None, **kwargs):
        """ Run the synchronization """
        if filters is None:
            filters = {}
        if 'limit' in filters:
            self._run_page(filters, **kwargs)
            return
        page_number = 0
        filters['limit'] = '%d,%d' % (
            page_number * self.page_size, self.page_size)
        record_ids = self._run_page(filters, **kwargs)
        while len(record_ids) == self.page_size:
            page_number += 1
            filters['limit'] = '%d,%d' % (
                page_number * self.page_size, self.page_size)
            record_ids = self._run_page(filters, **kwargs)

    def _run_page(self, filters, **kwargs):
        record_ids = self.backend_adapter.search(filters)

        for record_id in record_ids:
            self._import_record(record_id, **kwargs)
        return record_ids

    def _import_record(self, record):
        """ Import a record directly or delay the import of the record """
        raise NotImplementedError


@job(default_channel='root.tienda_nube')
def import_batch(session, model_name, backend_id, filters=None, **kwargs):
    """ Prepare a batch import of records from TiendaNube """
    backend = session.env['tienda_nube.backend'].browse(backend_id)
    env = backend.get_environment(model_name, session=session)
    importer = env.get_connector_unit(BatchImporter)
    importer.run(filters=filters, **kwargs)
