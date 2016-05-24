# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
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
#
# -----------------------------------------------------------------------------------
from openerp import models, fields, api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

BLK = 'black'


class res_users(models.Model):
    _inherit = 'res.users'

    colour_id = fields.Many2one('colour', 'Color')

    @api.model
    def is_black(self):
        return self.env.user.colour_id.name

    @api.model
    def create(self, vals):
        vals['colour_id'] = self.env.user.colour_id.id
        return super(res_users, self).create(vals)

    @api.one
    def onchange_colour(self, colour_id):
        parameter_obj = self.env['ir.config_parameter'].sudo()

        self.env.user.colour_id = colour_id
        if self.env.user.colour_id.name == BLK:
            parameter_obj.set_param('ribbon.name', BLK)
            parameter_obj.set_param('ribbon.background.color', 'rgba(0,0,0,0.6)')
        else:
            parameter_obj.set_param('ribbon.name', 'False')

    @api.v7
    def authenticate(self, db, login, password, user_agent_env):
        print 'autenticatte ----------------------------------------------------------'
        # obtengo el id del usuario
        uid = self._login(db, login, password)
        cr = self.pool.cursor()
        try:
            # busco el usuario por id
            usr_obj = self.pool['res.users']
            usr_ids = usr_obj.search(cr, SUPERUSER_ID, [('id', '=', uid)])
            usr = usr_obj.browse(cr, SUPERUSER_ID, usr_ids)

            # creo el objeto params
            params_obj = self.pool['ir.config_parameter']

            # le pongo el color del usuario
            if not usr.colour_id.name or usr.colour_id.name == BLK:
                print ' poner negro'
                params_obj.set_param(cr, SUPERUSER_ID, 'ribbon.name', BLK)
            else:
                print 'poner blanco'
                params_obj.set_param(cr, SUPERUSER_ID, 'ribbon.name', 'False')

            print 'color del usuario >>>', params_obj.get_param(cr, SUPERUSER_ID, 'ribbon.name')
            cr.commit()
        except Exception:
            _logger.exception("Failed to update ribbon.name configuration parameter")
        finally:
            cr.close()

        return super(res_users, self).authenticate(db, login, password, user_agent_env)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
