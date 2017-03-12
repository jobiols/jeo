# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from ...unit.deleter import TiendaNubeDeleter
from ...backend import tienda_nube


@tienda_nube
class ProductImageDelete(TiendaNubeDeleter):
    _model_name = 'tienda_nube.product.image'

    def delete(self, id):
        """ Delete a record on the external system """
        return self._call('%s.delete' % self._tienda_nube_model, [int(id)])
