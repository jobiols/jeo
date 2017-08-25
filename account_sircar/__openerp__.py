# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
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
    'name': 'SIRCAR',
    'version': '8.0.1.0',
    'category': 'Base',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

SIRCAR
======
Sistema de Recaudación y Control de Agentes de Recaudación

Este modulo genera un archivo de percepciones SIRCAR

con los siguientes campos harcodeados
campo 2 (tipo de comprobante) = 1
campo 8 (alicuota) = 1
campo 10 (tipo de regimen de retencion) = 10
campo 11 (jurisdiccion) = 916

depende de la localizacion adhoc

    """,
    'author': 'jeo Software',
    'depends': [
        'l10n_ar_invoice',
        'l10n_ar_account_vat_ledger'
    ],
    "data": [
        'views/account_sircar_report_view.xml',
    ],
    'website': 'http://jeosoft.com.ar',
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: