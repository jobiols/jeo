# -*- coding: utf-8 -*-
# #######################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
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
# #######################################################################
from openerp import models, fields
from openerp.addons.connector.checkpoint import checkpoint
from openerp.addons.connector.connector import Environment
import logging

_logger = logging.getLogger(__name__)


def add_checkpoint(session, model_name, record_id, backend_id):
    """ Add a row in the model ``connector.checkpoint`` for a record,
    meaning it has to be reviewed by a user.

    :param session: current session
    :type session: \
      :py:class:`openerp.addons.connector.session.ConnectorSession`
    :param model_name: name of the model of the record to be reviewed
    :type model_name: str
    :param record_id: ID of the record to be reviewed
    :type record_id: int
    :param backend_id: ID of the TiendaNube Backend
    :type backend_id: int
    """
    return checkpoint.add_checkpoint(session, model_name, record_id,
                                     'tienda_nube.backend', backend_id)


def get_environment(session, model_name, backend_id):
    """ Create an environment to work with. """
    print 'revisar get environment =========================================================='
    backend_record = session.env['tienda_nube.backend'].browse(backend_id)
    env = Environment(backend_record, session, model_name)
    lang = backend_record.default_lang_id
    lang_code = lang.code if lang else 'es_ES'
    if lang_code == session.context.get('lang'):
        return env
    else:
        with env.session.change_context(lang=lang_code):
            return env


class TiendaNubeBinding(models.AbstractModel):
    _name = 'tienda_nube.binding'
    _inherit = 'external.binding'
    _description = 'Tienda Nube Binding (abstract)'

    # 'openerp_id': openerp-side id must be declared in concrete model
    backend_id = fields.Many2one(
            comodel_name='tienda_nube.backend',
            string='Tienda Nube Backend',
            required=True,
            ondelete='restrict',
    )
    # fields.char because 0 is a valid tienda nube ID
    tienda_nube_id = fields.Char(string='ID in Tienda Nube', select=True)
