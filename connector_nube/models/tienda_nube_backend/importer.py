# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _
from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from ...unit.importer import TiendaNubeImporter, DirectBatchImporter
from ...backend import tienda_nube


@tienda_nube
class ShopGroupImportMapper(ImportMapper):
    _model_name = 'tienda_nube.shop.group'

    direct = [('name', 'name')]

    @mapping
    def name(self, record):
        name = record['name']
        if name is None:
            name = _('Undefined')
        return {'name': name}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}


@tienda_nube
class ShopGroupImporter(TiendaNubeImporter):
    _model_name = 'tienda_nube.shop.group'


@tienda_nube
class ShopGroupBatchImporter(DirectBatchImporter):
    _model_name = 'tienda_nube.shop.group'
