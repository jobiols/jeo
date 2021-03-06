# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
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
from openerp import models, api, fields, _
from ast import literal_eval
from openerp.exceptions import Warning

import datetime

####################################################
#Este código está deshabilitado en el __init__.py

class res_partner_update_from_padron_wizard(models.TransientModel):
    _name = 'res.partner.update.from.padron.wizard'

    @api.model
    def get_partners(self):
        #        print 'get partners ====================================================='
        domain = [
            ('document_number', '!=', False),
            ('document_type_id.afip_code', '=', 80),
            '|', ('last_update_padron', '!=', datetime.date.today().strftime('%Y-%m-%d')),
            ('last_update_padron', '=', False)
        ]
        active_ids = self._context.get('active_ids', [])
        if active_ids:
            domain.append(('id', 'in', active_ids))
        return self.env['res.partner'].search(domain, limit=2000)

    @api.model
    def default_get(self, fields):
        res = super(res_partner_update_from_padron_wizard, self).default_get(
            fields)
        context = self._context
        if (
                        context.get('active_model') == 'res.partner' and
                    context.get('active_ids')
        ):
            res['state'] = 'selection'
            partners = self.get_partners()
            if not partners:
                raise Warning(_(
                    'No se encontró ningún partner con CUIT para actualizar'))
            res['partner_id'] = partners[0].id
        return res

    @api.model
    def _get_domain(self):
        fields_names = [
            'name',
            'estado_padron',
            'street',
            'city',
            'zip',
            'actividades_padron',
            'impuestos_padron',
            'imp_iva_padron',
            'state_id',
            'imp_ganancias_padron',
            'monotributo_padron',
            'actividad_monotributo_padron',
            'empleador_padron',
            'integrante_soc_padron',
            'last_update_padron',
            # 'constancia',
        ]
        return [
            ('model', '=', 'res.partner'),
            ('name', 'in', fields_names),
        ]

    @api.model
    def get_fields(self):
        return self.env['ir.model.fields'].search(self._get_domain())

    state = fields.Selection([
        ('option', 'Option'),
        ('selection', 'Selection'),
        ('finished', 'Finished')],
        'State',
        readonly=True,
        required=True,
        default='option',
    )
    field_ids = fields.One2many(
        'res.partner.update.from.padron.field',
        'wizard_id',
        string='Fields',
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'partner_update_from_padron_rel',
        'update_id', 'partner_id',
        string='Partners',
        default=get_partners,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        readonly=True,
    )
    update_constancia = fields.Boolean(
        default=True,
    )
    field_to_update_ids = fields.Many2many(
        'ir.model.fields',
        'res_partner_update_fields',
        'update_id', 'field_id',
        string='Fields To Update',
        help='Only this fields are going to be retrived and updated',
        default=get_fields,
        domain=_get_domain,
        required=True,
    )

    @api.multi
    @api.onchange('partner_id')
    def change_partner(self):
        self.ensure_one()
        self.field_ids.unlink()
        partner = self.partner_id
        fields_names = self.field_to_update_ids.mapped('name')
        if partner:
            partner_vals = partner.get_data_from_padron_afip()
            lines = []
            # partner_vals.pop('constancia')
            for key, new_value in partner_vals.iteritems():
                old_value = getattr(partner, key)
                if new_value == '':
                    new_value = False
                if key in ('impuestos_padron', 'actividades_padron'):
                    old_value = old_value.ids
                elif key == 'state_id':
                    old_value = old_value.id
                if key in fields_names and old_value != new_value:
                    line_vals = {
                        'wizard_id': self.id,
                        'field': key,
                        'old_value': old_value,
                        # 'new_value': new_value,
                        'new_value': new_value or False,
                    }
                    lines.append((0, False, line_vals))
            self.field_ids = lines

    # @mute_logger('openerp.osv.expression', 'openerp.models')
    @api.multi
    def _update(self):
        """ Aca escribe los datos del padron en el partner
        hay veces que viene field.field == impuestos padron y field.new_value == False
        entonces revienta, le hago un parche
        """
        self.ensure_one()
        vals = {}
        for field in self.field_ids:
            if field.field in ('impuestos_padron', 'actividades_padron'):
                if field.new_value:
                    vals[field.field] = [(6, False, literal_eval(field.new_value))]
            else:
                vals[field.field] = field.new_value
            #        print 'valores a escribir==========:',vals
            #        print 'en el partner ==============:',self.partner_id.name
        # no actualizar si AFIP manda un registro en blanco
        write = True
        if 'name' in vals:
            if vals['name'] == False:
                write = False

        if write:
            self.partner_id.write(vals)
        if self.update_constancia:
            self.partner_id.update_constancia_from_padron_afip()

    @api.multi
    def automatic_process_cb(self):
        """
        Start the automatic process
        """
        self.start_process_cb()
        self.refresh()

        for partner in self.partner_ids:
            self._update()
            #           si dejamos esta linea se trae siempre el mismo partner
            #            partner = self.partner_ids[0]
            self.partner_id = partner.id
            self.change_partner()

        self.write({'state': 'finished'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def update_selection(self):
        self.ensure_one()
        if not self.field_ids:
            self.write({'state': 'finished'})
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
        self._update()
        return self.next_cb()

    @api.multi
    def next_cb(self):
        """
        """
        self.ensure_one()
        if self.partner_id:
            self.write({'partner_ids': [(3, self.partner_id.id, False)]})
        return self._next_screen()

    @api.multi
    def _next_screen(self):
        self.ensure_one()
        self.refresh()
        values = {}
        if self.partner_ids:
            # in this case, we try to find the next record.
            partner = self.partner_ids[0]
            values.update({
                'partner_id': partner.id,
                'state': 'selection',
            })
        else:
            values.update({
                'state': 'finished',
            })

        self.write(values)
        # because field is not changed, view is distroyed and reopen, on change
        # is not called an we call it manually
        self.change_partner()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def start_process_cb(self):
        """
        Start the process for manual update
        """
        self.ensure_one()
        return self._next_screen()
