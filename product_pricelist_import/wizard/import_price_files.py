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

import base64
import cStringIO
import tempfile
import csv

from openerp import fields, exceptions, models, api, _


class ImportPriceFile(models.TransientModel):
    _name = 'import.price.file'
    _description = 'Import Price List File'

    data = fields.Binary('File', required=True)
    name = fields.Char('Filename', required=False)
    delimeter = fields.Char('Delimeter', default=',', help='Default delimeter is ","')
    file_type = fields.Selection([('csv', 'CSV'),
                                  ('xls', 'XLS')],
                                 'File Type', required=True, default='xls')

    def get_indirection(self, kbd, kxl):
        """
        :param kbd: parametros de la base de datos
        :param kxl: parametros de la planilla de calculo
        :return: indice de indireccion que relaciona ambos
        """
        res = []
        for name in kbd:
            # para generar el indice uso dos criterios, uno que mapea nombres al principio
            # y otro posicional que relaciona los d1, d2 ... d6 con dp1, dp2, dc3 etc.
            positional = True if name[0] == 'd' else False
            if positional:
                # si estamos en modo posicional el indice es el numero siguiente.
                res.append(res[-1] + 1)
            else:
                # si estamos mapeando, el indice es la ubicación en kxl
                try:
                    res.append(kxl.index(name))
                except:
                    res.append('none')
        return res

    def append_file_lines(self, reader_info, load_id):
        file_line_obj = self.env['product.pricelist.load.line']
        # columnas de la bd
        keys_bd = ['product_code',
                   'product_name',
                   'product_description',
                   'list_price',
                   'prod_in_box',
                   'prod_in_box_uom',
                   'categ', 'sub_categ',
                   'd1', 'd2', 'd3', 'd4', 'd5', 'd6']

        # headers de la planilla
        keys_xls = reader_info[0]
        # calcula la indirección entre las dos claves
        indi = self.get_indirection(keys_bd, keys_xls)
        # elimina la fila de headers
        del reader_info[0]
        counter = 0
        for j in range(len(reader_info)):
            values = {}
            # arma un diccionario con los values y lo inserta en line
            for i in range(len(keys_bd)):
                # uso una indirección para conectar los datos
                if indi[i] <> 'none':
                    values[keys_bd[i]] = reader_info[j][indi[i]]
            values['fail'] = True
            values['fail_reason'] = _('No Processed')
            values['file_load'] = load_id
            file_line_obj.sudo().create(values)
            counter += 1
        return self.make_keystring(keys_xls), counter

    def make_keystring(self, keys_xls):
        # devuelve un keystring con los campos de los descuentos de la plantilla
        # son todos los que empiezan con dp dc o ds en el orden en el que aparecen
        res = []
        for key in keys_xls:
            s = key[:2]
            if s == 'dp' or s == 'dc' or s == 'ds':
                res.append(key)
        return ','.join(res)

    def _import_csv(self, load_id, file_data, delimiter=';'):
        """ Imports data from a CSV file in defined object.
        @param load_id: Loading id
        @param file_data: Input data to load
        @param delimiter: CSV file data delimiter
        @return: keys and Imported file number
        """
        file_line_obj = self.env['product.pricelist.load.line']
        data = base64.b64decode(file_data)
        file_input = cStringIO.StringIO(data)
        file_input.seek(0)
        reader_info = []
        reader = csv.reader(file_input, delimiter=str(delimiter),
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))

        return self.append_file_lines(reader_info, load_id)

    def _import_xls(self, load_id, file_data):
        """ Imports data from a XLS file in defined object.
        @param load_id: Loading id
        @param file_data: Input data to load
        @return: keys and Imported file number
        """

        try:
            import xlrd
        except ImportError:
            exceptions.Warning(_("xlrd python lib  not installed"))

        file_line_obj = self.env['product.pricelist.load.line']
        file_1 = base64.decodestring(file_data)
        (fileno, fp_name) = tempfile.mkstemp('.xls', 'openerp_')
        fp_name = '/etc/odoo/tst.xls'
        openfile = open(fp_name, "w")
        openfile.write(file_1)
        openfile.close()
        book = xlrd.open_workbook(fp_name)
        sheet = book.sheet_by_index(0)

        reader_info = []
        for counter in range(sheet.nrows):
            # grab the current row
            rowValues = sheet.row_values(counter, 0, end_colx=sheet.ncols)
            if counter != 0:
                if isinstance(rowValues[0], float):
                    rowValues[0] = str(int(rowValues[0]))

            if rowValues[0]:
                reader_info.append(rowValues)

        return self.append_file_lines(reader_info, load_id)

    @api.multi
    def action_import(self):
        file_load_obj = self.env['product.pricelist.load']
        context = self._context

        if 'active_id' in context:
            load_id = context['active_id']
            file_load = file_load_obj.browse(load_id)

        for line in file_load.file_lines:
            line.unlink()

        for wiz in self:
            if not wiz.data:
                raise exceptions.Warning(_("You need to select a file!"))

            date_hour = fields.datetime.now()

            actual_date = fields.date.today()
            filename = wiz.name
            if wiz.file_type == 'csv':
                keys, counter = self._import_csv(load_id, wiz.data, wiz.delimeter)
            elif wiz.file_type == 'xls':
                keys, counter = self._import_xls(load_id, wiz.data)
            else:
                raise exceptions.Warning(_("Not a .csv/.xls file found"))
            file_load.write({'name': ('%s_%s') % (filename, actual_date),
                             'date': date_hour, 'fails': counter,
                             'file_name': filename, 'process': counter, 'keys': keys})
        return counter
