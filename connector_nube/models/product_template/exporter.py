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


@job(default_channel='root.tienda_nube')
def export_product_quantities(session, ids):
    print 'product_template.exporter.export_product_quantities  -------------------------------'
    for model in ['template', 'combination']:
        model_obj = session.env['tienda_nube.product.' + model]
        model_obj.search([
            ('backend_id', 'in', [ids]),
        ]).recompute_tienda_nube_qty()


@job(default_channel='root.tienda_nube')
def export_inventory(session, model_name, record_id, fields=None):
    """ Export the inventory configuration and quantity of a product. """
    template = session.env[model_name].browse(record_id)
    backend_id = template.backend_id.id
    env = get_environment(session, model_name, backend_id)
    inventory_exporter = env.get_connector_unit(ProductInventoryExporter)
    return inventory_exporter.run(record_id, fields)
