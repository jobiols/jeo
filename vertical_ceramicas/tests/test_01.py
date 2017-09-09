# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------
# Forma de correr el test
# Crear un cliente test, una bd test_pricelist, el modulo test_pricelist_import cargado y
# un usuario admin / admin
# OJO cambiarle el path donde está el archivo a importar, esta en lugares distintos para travis o local
# ./odooenv.py -Q reves test_01.py -c reves -d reves_travis -m reves_default
from openerp.tests.common import SingleTransactionCase

class TestReves(SingleTransactionCase):
    def setUp(self):
        super(TestReves, self).setUp()

        # crear el wizard
        self.wizard = self.env['import.price.file'].create({
            'data': '1',
            'name': 'juan'
        })

    def test_01_1(self):
        pass

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
