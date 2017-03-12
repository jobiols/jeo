# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.connector.connector import Binder
from ..backend import tienda_nube


@tienda_nube
class TiendaNubeBinder(Binder):
    """
    Bindings are done directly on the model
    """
    _external_field = 'tienda_nube_id'
    _openerp_field = 'odoo_id'

    _model_name = [
        'tienda_nube.shop.group',
        'tienda_nube.shop',
        'tienda_nube.res.partner',
        'tienda_nube.address',
        'tienda_nube.res.partner.category',
        'tienda_nube.res.lang',
        'tienda_nube.res.country',
        'tienda_nube.res.currency',
        'tienda_nube.account.tax',
        'tienda_nube.account.tax.group',
        'tienda_nube.product.category',
        'tienda_nube.product.image',
        'tienda_nube.product.template',
        'tienda_nube.product.combination',
        'tienda_nube.product.combination.option',
        'tienda_nube.product.combination.option.value',
        'tienda_nube.sale.order',
        'tienda_nube.sale.order.state',
        'tienda_nube.delivery.carrier',
        'tienda_nube.refund',
        'tienda_nube.supplier',
        'tienda_nube.product.supplierinfo',
        'tienda_nube.mail.message',
        'tienda_nube.groups.pricelist',
    ]

    def to_odoo(self, external_id, unwrap=False):
        # Make alias to to_openep, remove in v10
        return self.to_openerp(external_id, unwrap)
