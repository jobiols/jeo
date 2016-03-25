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

from openerp import models, fields, exceptions, api, _


class ProductPricelistLoad(models.Model):
    _name = 'product.pricelist.load'
    _description = 'Product Price List Load'

    name = fields.Char('Load')
    date = fields.Date('Date:', readonly=True)
    file_name = fields.Char('File Name', readonly=True)
    file_lines = fields.One2many('product.pricelist.load.line', 'file_load',
                                 'Product Price List Lines')
    fails = fields.Integer('Fail Lines:', readonly=True)
    process = fields.Integer('Lines to Process:', readonly=True)
    supplier = fields.Many2one('res.partner')

    @api.multi
    def check_category(self, line):
        # TODO buscar primero por la categoria del proveedor
        # TODO si no la encuentro debería crearla

        print 1
        cat = self.category_obj.search([('name', '=', line.categ)])
        if not cat:
            cat = self.category_obj.create({'name': line.categ})

        print 2
        sub = cat.child_id.search([('name', '=', line.sub_categ)])
        if not sub:
            sub = cat.child_id.create({'name': line.sub_categ, 'parent_id': cat.id})

        print 3
        print sub.complete_name

        return True

    @api.multi
    def check_product(self, line):
        # actualizar producto
        product_lst = self.product_obj.search(
            [('default_code', '=', line.product_code)])
        if not product_lst:
            product_lst.create({'name': line.product_code,
                                'default_code': line.product_code,
                                'standard_price': line.list_price})
        else:
            product_lst.write({'standard_price': line.list_price})
        return True

    @api.multi
    def check_supplier(self, line):
        # buscar en suppinfo proveedor y codigo
        suppinfo = self.psupplinfo_obj.search(
            [('product_code', '=', line.product_code), ('name', '=', self.supplier.id)])
        if not suppinfo:
            # no existe, creamos el producto
            prod = self.product_obj.create({
                'default_code': line.product_code,
                'name': line.product_name,
                'type': 'product'
            })
            # creamos el proveedor
            self.psupplinfo_obj.create({
                'product_code': line.product_code,
                'name': self.supplier.id,
                'product_tmpl_id': prod.id
            })
        else:
            # si existia, tomamos el producto
            prod = suppinfo.product_tmpl_id

        # finalmente actualizamos el precio
        prod.standard_price = line.list_price

        return True

    @api.multi
    def process_line(self, line):
        if self.check_category(line):
            if self.check_supplier(line):
                return True
        return False

    @api.multi
    def process_lines(self):
        # ponerle a la instancia de la clase el nombre file_load
        for file_load in self:
            # si no le puse proveedor abortar
            if not file_load.supplier:
                raise exceptions.Warning(_("You must select a Supplier"))
            self.product_obj = self.env['product.product']
            self.psupplinfo_obj = self.env['product.supplierinfo']
            self.pricepinfo_obj = self.env['pricelist.partnerinfo']
            self.category_obj = self.env['product.category']

            if not file_load.file_lines:
                raise exceptions.Warning(_("There must be one line at least to"
                                           " process"))
            # procesar cada linea de file_load
            for line in file_load.file_lines:
                # procesar las lineas que estan en fail
                if line.fail:
                    if line.check():
                        if self.process_line(line):
                            line.write({
                                'fail': False,
                                'fail_reason': _('Processed Ok')})

            count = 0
            for line in file_load.file_lines:
                if line.fail:
                    count += 1
            file_load.fails = count

        return True


class ProductPricelistLoadLine(models.Model):
    _name = 'product.pricelist.load.line'
    _description = 'Product Price List Load Line'

    def check(self):
        # check product, must exist code and name
        if self.product_code and not self.product_name:
            self.fail_reason = _('Missing product name')
            return False
        if not self.product_code and self.product_name:
            self.fail_reason = _('Missing product code')
            return False
        if self.product_code and not self.list_price:
            self.fail_reason = _('Missing list price')
            return False
        if not self.product_code and self.list_price:
            self.fail_reason= _('Missing product')
            return False
        if not self.categ and self.sub_categ:
            self.fail_reason= _('Missing category')
            return False
        return True

    def standard_price(self):
        return self.list_price * (1-self.discount)

    product_code = fields.Char('Product Code', required=True)
    product_name = fields.Char('Product Name')
    list_price = fields.Float('List Price', required=True)
    categ = fields.Char('Category')
    sub_categ = fields.Char('Sub Category')
    discount = fields.Float('Discount %')
    fail = fields.Boolean('Fail')
    fail_reason = fields.Char('Fail Reason')
    file_load = fields.Many2one('product.pricelist.load', 'Load', required=True)
