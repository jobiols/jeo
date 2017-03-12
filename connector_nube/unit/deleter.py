# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.synchronizer import Deleter
from ..connector import get_environment


class TiendaNubeDeleter(Deleter):
    """ Base deleter for TiendaNube """

    def run(self, resource, external_id):
        """ Run the synchronization, delete the record on TiendaNube

        :param external_id: identifier of the record to delete
        """
        self.backend_adapter.delete(resource, external_id)
        return _('Record %s deleted on TiendaNube on resource %s') % (
            external_id, resource)


TiendaNubeDeleteSynchronizer = TiendaNubeDeleter  # Deprecated


@job(default_channel='root.tienda_nube')
def export_delete_record(
        session, model_name, backend_id, external_id, resource):
    """ Delete a record on TiendaNube """
    env = get_environment(session, model_name, backend_id)
    deleter = env.get_connector_unit(TiendaNubeDeleter)
    return deleter.run(resource, external_id)
