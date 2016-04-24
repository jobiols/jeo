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
from openerp import fields, models, api, _
from openerp.exceptions import Warning

class ImportPriceFile(models.TransientModel):
    _name = 'import.price.file'
    _description = 'Import Price List File'

    data = fields.Binary('File', required=True)
    name = fields.Char('Filename', required=False)
    delimeter = fields.Char('Delimeter', default=',', help='Default delimeter is ","')
    file_type = fields.Selection([('csv', 'CSV'),
                                  ('xls', 'XLS')],
                                 'File Type', required=True, default='xls')

    def append_file_lines(self, reader_info, load_id):
        file_line_obj = self.env['product.pricelist.load.line']
        keys1 = ['product_code', 'product_name', 'list_price', 'categ', 'sub_categ', 'd1',
                 'd2', 'd3', 'd4', 'd5', 'd6']
        keys = reader_info[0]
        del reader_info[0]

        counter = 0
        for i in range(len(reader_info)):
            values = dict(zip(keys1, reader_info[i]))
            values['fail'] = True
            values['fail_reason'] = _('No Processed')
            values['file_load'] = load_id
            file_line_obj.create(values)
            counter += 1
        kstring = ','.join(keys)
        return kstring, counter

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
        values = {}
        keys = ['product_code', 'product_name', 'list_price', 'categ', 'sub_categ', 'd1',
                'd2', 'd3', 'd4', 'd5', 'd6', ]
        # keys2 = sheet.row_values(0,0, end_colx=sheet.ncols)
        reader_info = []
        for counter in range(sheet.nrows):
            # grab the current row
            rowValues = sheet.row_values(counter, 0, end_colx=sheet.ncols)
            if counter != 0:
                if isinstance(rowValues[0], float):
                    rowValues[0] = str(int(rowValues[0]))

            if rowValues[0]:
                reader_info.append(rowValues)

            if False:
                rowResults = []
                if isinstance(rowValues[0], float):
                    rowResults.append(str(int(rowValues[0])))
                else:
                    rowResults.append(rowValues[0])

                for cell in rowValues[1:]:
                    if isinstance(cell, basestring):
                        rcell = cell.encode('utf-8')
                    else:
                        rcell = str(cell)
                    rowResults.append(rcell)
                row = rowResults
                values = dict(zip(keys, row))
                values['fail'] = True
                values['fail_reason'] = _('No Processed')
                values['file_load'] = load_id
                file_line_obj.create(values)
                counter += 1
                return keys, counter - 1
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
