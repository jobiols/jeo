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
from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from ...unit.importer import (
    import_record,
    DelayedBatchImporter,
    TranslatableRecordImporter
)
from ...backend import tienda_nube


@tienda_nube
class PartnerCategoryImportMapper(ImportMapper):
    _model_name = 'tienda_nube.res.partner.category'

    direct = [
        ('name', 'name'),
        ('date_add', 'date_add'),
        ('date_upd', 'date_upd'),
    ]

    @mapping
    def tienda_nube_id(self, record):
        return {'tienda_nube_id': record['id']}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}


@tienda_nube
class PartnerCategoryRecordImport(TranslatableRecordImporter):
    """ Import one translatable record """
    _model_name = [
        'tienda_nube.res.partner.category',
    ]

    _translatable_fields = {
        'tienda_nube.res.partner.category': ['name'],
    }

    def _after_import(self, erp_id):
        record = self._get_tienda_nube_data()
        if float(record['reduction']):
            import_record(
                self.session,
                'tienda_nube.groups.pricelist',
                self.backend_record.id,
                record['id']
            )


@tienda_nube
class PartnerCategoryBatchImporter(DelayedBatchImporter):
    _model_name = 'tienda_nube.res.partner.category'
