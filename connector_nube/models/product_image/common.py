# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import base64

from openerp import models, fields

from ...unit.backend_adapter import (
    TiendaNubeCRUDAdapter,
    TiendaNubeWebServiceImage,
)
from ...backend import tienda_nube

_logger = logging.getLogger(__name__)


class ProductImage(models.Model):
    _inherit = 'base_multi_image.image'

    tienda_nube_bind_ids = fields.One2many(
            comodel_name='tienda_nube.product.image',
            inverse_name='odoo_id',
            string='TiendaNube Bindings',
    )


class TiendaNubeProductImage(models.Model):
    _name = 'tienda_nube.product.image'
    _inherit = 'tienda_nube.binding.odoo'
    _inherits = {'base_multi_image.image': 'odoo_id'}

    odoo_id = fields.Many2one(
            comodel_name='base_multi_image.image',
            required=True,
            ondelete='cascade',
            string='Product image',
            oldname='openerp_id',
    )


@tienda_nube
class ProductImageAdapter(TiendaNubeCRUDAdapter):
    _model_name = 'tienda_nube.product.image'
    _tienda_nube_image_model = 'products'
    _tienda_nube_model = '/images/products'
    _export_node_name = '/images/products'

    def read(self, product_tmpl_id, image_id, options=None):
        api = TiendaNubeWebServiceImage(self.tienda_nube.api_url,
                                        self.tienda_nube.webservice_key)
        return api.get_image(
                self._tienda_nube_image_model,
                product_tmpl_id,
                image_id,
                options=options
        )

    def create(self, attributes=None):
        api = TiendaNubeWebServiceImage(
                self.tienda_nube.api_url, self.tienda_nube.webservice_key)
        template_binder = self.binder_for('tienda_nube.product.template')
        template = template_binder.to_backend(
                attributes['id_product'], wrap=True)
        url = '{}/{}'.format(self._tienda_nube_model, template)
        return api.add(url, files=[(
            'image',
            attributes['filename'].encode('utf-8'),
            base64.b64decode(attributes['content'])
        )])

    def write(self, id, attributes=None):
        api = TiendaNubeWebServiceImage(
                self.tienda_nube.api_url, self.tienda_nube.webservice_key)
        template_binder = self.binder_for('tienda_nube.product.template')
        template = template_binder.to_backend(
                attributes['id_product'], wrap=True)
        url = '{}/{}'.format(self._tienda_nube_model, template)
        url_del = '{}/{}/{}/{}'.format(
                api._api_url, self._tienda_nube_model, template, id)
        try:
            api._execute(url_del, 'DELETE')
        except:
            pass
        return api.add(url, files=[(
            'image',
            attributes['filename'].encode('utf-8'),
            base64.b64decode(attributes['content'])
        )])

    def delete(self, resource, id):
        """ Delete a record on the external system """
        api = TiendaNubeWebServiceImage(
                self.tienda_nube.api_url, self.tienda_nube.webservice_key)
        return api.delete(resource, resource_ids=id)
