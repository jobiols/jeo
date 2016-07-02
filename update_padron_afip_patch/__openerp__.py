# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    'name': 'Update padron apfip patch',
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Le pone un patch al modulo l10n_ar_padron_afip',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Patch a la actualización desde el padron
========================================

Cuando se actualizan muchos partners en automático siempre termina mal con algun
error, este patch no actualiza los partners que tienen fecha de actualización igual
a la de hoy.
De esa forma se puede correr varias veces y no vuelva a bajar lo mismo.
""",
    'author': 'jeo Software',
    'website': 'http://www.jeo-soft.com.ar',
    'depends': ['l10n_ar_padron_afip'],
    'data': [],
    'test': [],
    'installable': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
