# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.synchronizer import ExportSynchronizer

from ...unit.backend_adapter import GenericAdapter
from ...connector import get_environment
from ...backend import tienda_nube


@tienda_nube
class ProductInventoryExporter(ExportSynchronizer):
    _model_name = ['tienda_nube.product.template']

    def get_filter(self, template):
        binder = self.binder_for()
        tienda_nube_id = binder.to_backend(template.id)
        return {
            'filter[id_product]': tienda_nube_id,
            'filter[id_product_attribute]': 0
        }

    def run(self, binding_id, fields):
        """ Export the product inventory to TiendaNube """
        template = self.env[self.model._name].browse(binding_id)
        adapter = self.unit_for(GenericAdapter, '_import_stock_available')
        filter = self.get_filter(template)
        adapter.export_quantity(filter, int(template.quantity))


@job(default_channel='root.tienda_nube')
def export_inventory(session, model_name, record_id, fields=None):
    """ Export the inventory configuration and quantity of a product. """
    template = session.env[model_name].browse(record_id)
    backend_id = template.backend_id.id
    env = get_environment(session, model_name, backend_id)
    inventory_exporter = env.get_connector_unit(ProductInventoryExporter)
    return inventory_exporter.run(record_id, fields)


@job(default_channel='root.tienda_nube')
def export_product_quantities(session, ids):
    for model in ['template', 'combination']:
        model_obj = session.env['tienda_nube.product.' + model]
        model_obj.search([
            ('backend_id', 'in', [ids]),
        ]).recompute_tienda_nube_qty()
