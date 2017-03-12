# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.addons.connector.queue.job import job
from openerp.addons.connector.unit.synchronizer import Exporter
from ...connector import get_environment
from ...backend import tienda_nube


@tienda_nube
class SaleStateExporter(Exporter):
    _model_name = ['tienda_nube.sale.order']

    def run(self, tienda_nube_id, state):
        datas = {
            'order_history': {
                'id_order': tienda_nube_id,
                'id_order_state': state,
            }
        }
        self.backend_adapter.update_sale_state(tienda_nube_id, datas)


def find_tienda_nube_state(session, sale_state, backend_id):
    state_list_obj = session.env['sale.order.state.list']
    states_list = state_list_obj.search([
        ('name', '=', sale_state),
    ])
    for state_list in states_list:
        if state_list.tienda_nube_state_id.backend_id.id == backend_id:
            return state_list.tienda_nube_state_id.tienda_nube_id
    return None


@job
def export_sale_state(session, record_id):
    inherit_model = 'tienda_nube.sale.order'
    sales = session.env[inherit_model].search([('odoo_id', '=', record_id)])
    for sale in sales:
        backend_id = sale.backend_id.id
        new_state = find_tienda_nube_state(session, sale.state, backend_id)
        if new_state is None:
            continue
        env = get_environment(session, inherit_model, backend_id)
        sale_exporter = env.unit_for(SaleStateExporter)
        sale_exporter.run(sale.tienda_nube_id, new_state)
