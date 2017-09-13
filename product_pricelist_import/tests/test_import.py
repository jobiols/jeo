# -*- coding: utf-8 -*-
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
###################################################################################
from openerp.tests.common import SingleTransactionCase
import time


class TestPricelistImport(SingleTransactionCase):
    def setUp(self):
        super(TestPricelistImport, self).setUp()
        # creo una categoria para el proveedor
        self.categ1 = self.env['product.category'].create({
            'name': 'proovedor 1'
        })
        # creo un proveedor
        self.proveedor1 = self.env['res.partner'].create({
            'name': 'proveedor uno',
            'categ_id': self.categ1.id
        })
        # creo el product pricelist 1 y 2
        self.product_pricelist_load1 = self.env['product.pricelist.load'].create({
            'name': 'Archivo de prueba 1',
            'date': time.strftime('%Y-%m-%d'),
            'file_name': 'product_pricelist_import/tests/test_pricelist_1.csv',
            'supplier': self.proveedor1.id,
            'mode': 'append'
        })
        self.product_pricelist_load2 = self.env['product.pricelist.load'].create({
            'name': 'Archivo de prueba 2',
            'date': time.strftime('%Y-%m-%d'),
            'file_name': 'product_pricelist_import/tests/test_pricelist_2.csv',
            'supplier': self.proveedor1.id,
            'mode': 'no_append'
        })

    def test_01(self):
        """ Cargamos lista de precios 1
        """
        from datetime import datetime
        import base64
        import csv

        product_pricelist_load = self.env['product.pricelist.load'].browse(
            self.product_pricelist_load1.id)

        # leer el archivo
        CSVFILE = product_pricelist_load.file_name
        reader = csv.reader(open(CSVFILE, 'rb'), delimiter=',', lineterminator='\r\n')

        reader_info = []
        reader_info.extend(reader)

        import_price_file_obj = self.env['import.price.file']
        ids = import_price_file_obj.create({'data': 'a'})
        import_price_file = import_price_file_obj.browse(ids)

        # importar las lineas
        keys, counter = import_price_file.append_file_lines(reader_info,
                                                            self.product_pricelist_load1.id)
        product_pricelist_load.write({'name': 'test',
                                      'fails': counter,
                                      'process': counter,
                                      'keys': keys})

        product_pricelist_load.process_lines()

    def test_02(self):
        """ Chequeamos lista de precios 1
        """
        product_obj = self.env['product.product']
        print 'P01',
        records = product_obj.search([('default_code', '=', 'P01')])
        assert len(records) > 0, 'no se encuentra producto P01'
        for rec in records:
            print rec.standard_price
            assert rec.standard_price == 9.0, "falla calculo de precio de compra debe ser 9.0"

        print 'P02',
        records = product_obj.search([('default_code', '=', 'P02')])
        assert len(records) > 0, 'no se encuentra producto P02'
        for rec in records:
            print rec.standard_price
            assert rec.standard_price == 17.29, "falla calculo de precio de compra debe ser 17.29"

        print 'P03',
        records = product_obj.search([('default_code', '=', 'P03')])
        assert len(records) > 0, 'no se encuentra producto P03'
        for rec in records:
            print rec.standard_price
            assert rec.standard_price == 24.16, "falla calculo de precio de compra debe ser 24.16"

    def test_03(self):
        """ Cargamos lista de precios 2
        """
        from datetime import datetime
        import base64
        import csv

        product_pricelist_load = self.env['product.pricelist.load'].browse(
            self.product_pricelist_load2.id)

        # leer el archivo
        CSVFILE = product_pricelist_load.file_name
        reader = csv.reader(open(CSVFILE, 'rb'), delimiter=',', lineterminator='\r\n')

        reader_info = []
        reader_info.extend(reader)

        import_price_file_obj = self.env['import.price.file']
        ids = import_price_file_obj.create({'data': 'a'})
        import_price_file = import_price_file_obj.browse(ids)

        # importar las lineas
        keys, counter = import_price_file.append_file_lines(reader_info,
                                                            self.product_pricelist_load2.id)
        product_pricelist_load.write({'name': 'test',
                                      'fails': counter,
                                      'process': counter,
                                      'keys': keys})

        product_pricelist_load.process_lines()




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
