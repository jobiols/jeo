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
    'version': '8.0.1.0.2',
    'category': 'Tools',
    'summary': 'Customización Herrajes Valente',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Customización Herrajes Valente
================================
""",
    'author': 'jeo Software',
    'depends': [
        'l10n_ar_base',  # modulo base para localización argentina
        'base_vat_unique',  # evita que duplique cuit
        #        'base_vat_unique_parent',  # evita que duplique cuit en multicompañia
        'disable_openerp_online',  # elimina referencias a odoo online
        'account_cancel',  # Muestra el check en los diarios que permite cancelar asientos
        'product_pricelist_import',  # Importa lista de precios y carga productos
        'hide_product_variants',  # oculta las variantes
        'express_checkout',  # Facturación express
        'invoice_order_by_id',  # ordena facturas ultima arriba
        'account_invoice_tax_wizard',  # agrega menu add_taxes para cargar percepciones
        'sale_order_recalculate_prices',  # agrega boton para recalcular precios
        'consult_product_price',  # consulta de precios
        #        'account_journal_sequence'         # agrega un campo de secuencia en el diario para elegirlos
        #        'account_statement_move_import'    # agrega boton de importar aputnes en extractos bancarios
        'account_journal_sequence', #Adds sequence field on account journal and it is going to be considered when choosing journals in differents models.
        'l10n_ar_aeroo_sale',  # dependencia requerida
        'l10n_ar_aeroo_purchase',  # dependencia requerida
        'l10n_ar_aeroo_einvoice',  # dependencia requerida
        'l10n_ar_aeroo_stock',  # dependencia requerida
        'po_custom_reports',  # dependencia requerida
    ],
    'data': [
        'security/security_groups.xml',
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/default_values.xml',
        'views/custom_reports.xml',
        'views/invoice_view.xml',
        'views/sale_view.xml',
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
