# -*- coding: utf-8 -*-
########################################################################333###
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
########################################################################333###
{
    'name': 'Herrajes Valente',
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Customización Herrajes Valente',
    'description': """
Customización Herrajes Valente
================================

""",
    'author': 'jeo software',
    'depends': [
        'l10n_ar_base',
                'disable_openerp_online',
                'account_cancel',
                'product_pricelist_import',
                'hide_product_variants',
                'express_checkout',
        'invoice_order_by_id',
        'base_vat_unique'],
    'data': [
        'security/security_groups.xml',
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/hide_menus.xml', ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
