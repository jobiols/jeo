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
{
    "name": "Patch for odoo Argentina",
    "version": "8.0.0.1.0",
    "author": "jeo Software",
    'website': 'http://www.jeosoft.com.ar',
    "depends": ['l10n_ar_base', 'l10n_ar_padron_afip', 'account_cancel'],
    "category": "Generic Modules",
    "description": """
Localización Argentina Fix
==========================
Este módulo corrige algunos bugs encontrados en la localización

- Cuando se hace un reintegro de nota de crédito crea una nota de crédito. Se ocultó el botón reintegrar en ese caso.

Deshabilitamos esta ultima opción porque algo cambió y revienta cuando quiero
actualizar desde padron. Habrá que revisarlo.

- Cuando se actualizan muchos partners en automático siempre termina mal con algun
error, con este patch no actualiza los partners que tienen fecha de actualización igual
a la de hoy. De esa forma se puede correr varias veces y no vuelva a bajar lo mismo.


""",
    "demo_xml": [],
    "data": [
        'views/account_invoice_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
