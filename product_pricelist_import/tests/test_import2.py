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
import time
import base64

import xlrd
from openerp.tests.common import SingleTransactionCase
from openerp import fields
from file_location import PATH

# Este test verifica que funciona con las columnas opcionales agregadas

# Forma de correr el test
# Crear un cliente test, una bd test_pricelist, los modulos test_pricelist_import y
# reves_default cargados y un usuario admin / admin
# OJO cambiarle el path donde está el archivo a importar, esta en lugares distintos para travis o local
# ./odooenv.py -Q jeo test_import2.py -c test -d test_pricelist -m product_pricelist_import
#
# El test lee una planilla xls con formato Valente y verifica los costos contra los calculados
# por la planilla, tiene que resisir el agregado de dos columnas para el formato reves

class TestPricelistImport(SingleTransactionCase):
    def setUp(self):
        super(TestPricelistImport, self).setUp()

        # creo una categoria para el proveedor
        self.categ2 = self.env['product.category'].create({
            'name': 'prov2'
        })
        # creo un proveedor
        self.proveedor2 = self.env['res.partner'].create({
            'name': 'proveedor dos',
            'categ_id': self.categ2.id
        })
        # creo el product pricelist 2 (REVES)
        self.product_pricelist_load2 = self.env['product.pricelist.load'].create({
            'name': 'Archivo de prueba 2',
            'date': time.strftime('%Y-%m-%d'),
            'file_name': PATH + 'product_pricelist_import/tests/test_calc_2.xls',
            'supplier': self.proveedor2.id,
            'mode': 'append'
        })
        # el archivo a leer está en lugares distintos localmente y en travis
        # en local esta en / y en travis está en el dir donde está el repo

    def test_01(self):
        """ TEST 01 testear con archivo xls REVES ---------------------------------
        """

        # crear el wizard
        self.wizard = self.env['import.price.file'].create({
            'data': '1',
            'name': self.product_pricelist_load2.file_name
        })

        # leer el xls y codificarlo b64 para darselo al _import_xls
        with open(self.wizard.name, 'rb') as f:
            file_data = f.read()
        file_data_encoded = base64.b64encode(file_data)

        # importar xls
        keys, counter = self.wizard._import_xls(self.product_pricelist_load2.id,
                                                file_data_encoded)
        self.product_pricelist_load2.write(
            {'name': 'nombre de la carga',
             'date': fields.datetime.now(),
             'fails': counter,
             'file_name': self.product_pricelist_load2.file_name,
             'process': counter,
             'keys': keys}
        )

        # procesar las lineas
        self.product_pricelist_load2.process_lines()

    def test_02(self):
        """ TEST 02 verificar los descuentos contra la planilla REVES + m2 ---------------
        """
        # verificar categorias

        # verificar categorias
        #        print '******************listado de categorias************************************'
        #        categs = self.env['product.category'].search([])
        #        for categ in categs:
        #            print ''
        #            print u'{} {} {:10} {}'.format(categ.parent_id, categ.id,categ.name, categ.get_discount())
        #            for parent in categ.parent_id:
        #                print '-parent-- {} {} >'.format(parent.name, parent.get_discount()),parent
        #            for disc in categ.discounts:
        #                print '>discounts>> {} {} >'.format(disc.name, disc.discount),disc


        # Obtener los precios de costo de la planilla
        # Obtener producto por caja y unidad de medida de la planilla
        book = xlrd.open_workbook(self.product_pricelist_load2.file_name)
        sheet = book.sheet_by_index(0)

        product_obj = self.env['product.product']
        # chequear para cada fila de la tabla los costos calculados
        for row in range(1, sheet.nrows):
            prod = sheet.cell_value(rowx=row, colx=0)
            desc = sheet.cell_value(rowx=row, colx=2)
            m2 = sheet.cell_value(rowx=row, colx=4)
            uom = sheet.cell_value(rowx=row, colx=5)
            cost = sheet.cell_value(rowx=row, colx=15)
            records = product_obj.search([('default_code', '=', prod)])
            assert len(records) > 0, 'No se encuentra producto ' + prod
            for rec in records:
                diff = rec.standard_price - cost
                assert abs(
                    diff) < 0.01, u"Mal precio costo producto {} precio {} deberia ser {}".format(
                    rec.default_code,
                    rec.standard_price,
                    cost)
                assert desc == rec.description, u'Mal la descripción del producto'
                assert m2 == rec.prod_in_box, u'Mal cantidad producto en caja {} debería ser {}'.format(
                    rec.prod_in_box, m2
                )
                assert uom == rec.prod_in_box_uom, u'falla unidad de medida {} debería ser {}'.format(
                    rec.prod_in_box_uom, uom
                )