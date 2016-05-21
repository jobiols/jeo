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
from openerp import models, fields, api


class res_users(models.Model):
    _inherit = 'res.users'

    colour_id = fields.Many2one('colour', 'Color')

    @api.model
    def create(self, vals):
        vals['colour_id'] = self.env.user.colour_id.id
        print ' res_users >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ', vals
        return super(res_users, self).create(vals)

    @api.one
    def onchange_colour(self, colour_id):
        parameter_obj = self.env['ir.config_parameter'].sudo()

        self.env.user.colour_id = colour_id
        if self.env.user.colour_id.name == 'black':
            parameter_obj.set_param('ribbon.name', 'Negro')
            parameter_obj.set_param('ribbon.background.color', 'rgba(0,0,0,0.6)')
        else:
            parameter_obj.set_param('ribbon.name', 'False')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
