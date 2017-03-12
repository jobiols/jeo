# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from ...backend import tienda_nube
from ..product_template.exporter import ProductInventoryExporter


@tienda_nube
class CombinationInventoryExporter(ProductInventoryExporter):
    _model_name = ['tienda_nube.product.combination']

    def get_filter(self, template):
        return {
            'filter[id_product]': template.main_template_id.tienda_nube_id,
            'filter[id_product_attribute]': template.tienda_nube_id,
        }
