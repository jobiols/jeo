# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from ...unit.importer import TranslatableRecordImporter, DirectBatchImporter
from ...backend import tienda_nube


@tienda_nube
class SaleOrderStateMapper(ImportMapper):
    _model_name = 'tienda_nube.sale.order.state'

    direct = [
        ('name', 'name'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}


@tienda_nube
class SaleOrderStateImport(TranslatableRecordImporter):
    """ Import one translatable record """
    _model_name = [
        'tienda_nube.sale.order.state',
    ]

    _translatable_fields = {
        'tienda_nube.sale.order.state': [
            'name',
        ],
    }


@tienda_nube
class SaleOrderStateBatchImporter(DirectBatchImporter):
    _model_name = 'tienda_nube.sale.order.state'
