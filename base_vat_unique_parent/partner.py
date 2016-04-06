# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
##############################################################################
from osv import osv
from osv import fields


class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"

    def copy(self, cr, uid, id, default=None, context=None):
        '''
        When a copy of the Partner is made, the vat is set to None since it cannot be duplicated
        '''
        if default is None:
            default = {}
        default['vat'] = None
        return super(res_partner, self).copy(cr, uid, id, default=default,
                                             context=context)

    def _construct_constraint_msg_vat_partner(self, cr, uid, ids, context=None):
        partner = self.browse(cr, uid, ids)[0]
        if not partner.vat:
            return None

        company_id = False
        if partner.company_id:
            company_id = partner.company_id.id

        if company_id:
            eq_vat_ids = self.search(cr, uid, [('vat', '=', partner.vat),
                                               ('company_id', '=', company_id)],
                                     context=context)
        else:
            eq_vat_ids = self.search(cr, uid, [('vat', '=', partner.vat)],
                                     context=context)

        first_eq_vat_partner_id = eq_vat_ids[0]
        first_eq_vat_partner = self.browse(cr, uid, first_eq_vat_partner_id,
                                           context=context)
        msg = 'Ya existe un Partner %s con ese número de CUIT. Para poder usar el mismo CUIT (VAT) este partner debe ser hijo de %s'
        msg = msg % (first_eq_vat_partner.name.encode('utf-8'),
                     first_eq_vat_partner.name.encode('utf-8'))
        return msg.decode('utf-8')

    def check_vat_partner(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if not partner.vat:
                continue

            if not self.check_vat_correct(cr, uid, partner.vat, partner.id,
                                          context=context):
                return False
        return True

    _constraints = [
        (check_vat_partner, _construct_constraint_msg_vat_partner, ["vat", "partner_id"])]

    def check_vat_correct(self, cr, uid, vat, partner_id, context=None):
        company_id = False
        partner = self.browse(cr, uid, partner_id, context=context)
        if partner.company_id:
            company_id = partner.company_id.id

        if company_id:
            eq_vat_ids = self.search(cr, uid,
                                     [('vat', '=', vat), ('company_id', '=', company_id)],
                                     context=context)
        else:
            eq_vat_ids = self.search(cr, uid, [('vat', '=', vat)], context=context)

        if partner_id in eq_vat_ids:
            eq_vat_ids.remove(partner_id)
        if eq_vat_ids:
            connected = self.get_all_conected_with_vat(cr, uid, partner_id, vat,
                                                       context=context)
            if partner_id in connected:
                connected.remove(partner_id)

            if set(connected).intersection(set(eq_vat_ids)) == set():
                return False
        return True

    # Return of parents and children of given partner that have some specific vat
    def get_all_conected_with_vat(self, cr, uid, partner_id, vat, context=None):
        res = []
        partner = self.browse(cr, uid, partner_id, context=context)
        connected = self.get_all_conected(partner)
        for partner_it in self.browse(cr, uid, connected, context=context):
            if partner_it.vat == vat:
                res.append(partner_it.id)
        return res

    # Return of parents and children of given partner 
    def get_all_conected(self, partner):
        parents = self.get_all_parents(partner)
        children = self.get_all_children(partner)
        parents_set = set(parents)
        children_set = set(children)
        connected_set = parents_set.union(children_set)
        return list(connected_set)

    # Return of parents of given partner 
    def get_all_parents(self, partner):
        if not partner.parent_id:
            return []

        partners = []
        partner_it = partner.parent_id
        while True:
            partners.append(partner_it.id)

            if not partner_it.parent_id:
                break
            if partner_it.parent_id.id in partners:
                break

            partner_it = partner_it.parent_id

        return partners

    # Return of children of given partner 
    def get_all_children(self, partner):
        return self.get_all_children_inner(partner, [])

    def get_all_children_inner(self, partner, visited_children):
        if not partner or not partner.child_ids:
            return visited_children

        for child in partner.child_ids:
            if not child.id in visited_children:
                visited_children.append(child.id)
                sub_list = self.get_all_children_inner(child, visited_children)
                visited_children.extend(sub_list)

        return visited_children


res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
